#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务生命周期管理 (Task Lifecycle Management)

支持对计算执行环境任务创建、运行、暂停/重启、终止、归档以及销毁等过程的全生命周期管理与控制
"""

from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json


class TaskState(Enum):
    """任务状态"""
    CREATED = "created"
    CONFIGURED = "configured"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    TERMINATED = "terminated"
    ARCHIVED = "archived"
    DESTROYED = "destroyed"
    ERROR = "error"


class TaskTransition(Enum):
    """任务状态转换"""
    CREATE = "create"
    CONFIGURE = "configure"
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    TERMINATE = "terminate"
    ARCHIVE = "archive"
    DESTROY = "destroy"


@dataclass
class ResourceRequirements:
    """资源需求"""
    cpu_cores: int = 1
    memory_mb: int = 1024
    storage_mb: int = 10240
    network_bandwidth_mbps: float = 100.0
    gpu_count: int = 0
    custom_resources: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskConfig:
    """任务配置"""
    name: str
    description: str = ""
    resources: ResourceRequirements = field(default_factory=ResourceRequirements)
    initial_state: Dict[str, Any] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskEvent:
    """任务事件"""
    timestamp: datetime
    event_type: str
    state_from: TaskState
    state_to: TaskState
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class Task:
    """数字虚拟化任务"""
    
    def __init__(self, config: TaskConfig):
        self.task_id = str(uuid.uuid4())
        self.config = config
        self.state = TaskState.CREATED
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.terminated_at: Optional[datetime] = None
        self.events: List[TaskEvent] = []
        self.runtime_data: Dict[str, Any] = {}
        
        self._record_event(TaskTransition.CREATE.value, TaskState.CREATED, TaskState.CREATED)
    
    def configure(self, config_updates: Dict[str, Any]) -> bool:
        """配置任务"""
        if self.state not in [TaskState.CREATED, TaskState.CONFIGURED]:
            return False
        
        try:
            # 更新配置
            if "resources" in config_updates:
                self.config.resources = ResourceRequirements(**config_updates["resources"])
            if "environment" in config_updates:
                self.config.environment.update(config_updates["environment"])
            if "metadata" in config_updates:
                self.config.metadata.update(config_updates["metadata"])
            
            old_state = self.state
            self.state = TaskState.CONFIGURED
            self.updated_at = datetime.now()
            self._record_event(TaskTransition.CONFIGURE.value, old_state, self.state)
            return True
        except Exception as e:
            self._record_event("configure_error", self.state, TaskState.ERROR, str(e))
            return False
    
    def start(self) -> bool:
        """启动任务"""
        if self.state not in [TaskState.CONFIGURED, TaskState.READY]:
            return False
        
        old_state = self.state
        self.state = TaskState.RUNNING
        self.started_at = datetime.now()
        self.updated_at = datetime.now()
        self._record_event(TaskTransition.START.value, old_state, self.state)
        return True
    
    def pause(self) -> bool:
        """暂停任务"""
        if self.state != TaskState.RUNNING:
            return False
        
        old_state = self.state
        self.state = TaskState.PAUSED
        self.updated_at = datetime.now()
        self._record_event(TaskTransition.PAUSE.value, old_state, self.state)
        return True
    
    def resume(self) -> bool:
        """恢复任务"""
        if self.state != TaskState.PAUSED:
            return False
        
        old_state = self.state
        self.state = TaskState.RUNNING
        self.updated_at = datetime.now()
        self._record_event(TaskTransition.RESUME.value, old_state, self.state)
        return True
    
    def terminate(self) -> bool:
        """终止任务"""
        if self.state in [TaskState.TERMINATED, TaskState.ARCHIVED, TaskState.DESTROYED]:
            return False
        
        old_state = self.state
        self.state = TaskState.TERMINATED
        self.terminated_at = datetime.now()
        self.updated_at = datetime.now()
        self._record_event(TaskTransition.TERMINATE.value, old_state, self.state)
        return True
    
    def archive(self) -> bool:
        """归档任务"""
        if self.state != TaskState.TERMINATED:
            return False
        
        old_state = self.state
        self.state = TaskState.ARCHIVED
        self.updated_at = datetime.now()
        self._record_event(TaskTransition.ARCHIVE.value, old_state, self.state)
        return True
    
    def destroy(self) -> bool:
        """销毁任务"""
        if self.state == TaskState.DESTROYED:
            return False
        
        old_state = self.state
        self.state = TaskState.DESTROYED
        self.updated_at = datetime.now()
        self._record_event(TaskTransition.DESTROY.value, old_state, self.state)
        return True
    
    def clone(self, new_name: Optional[str] = None) -> 'Task':
        """克隆任务"""
        # 创建新配置
        new_config = TaskConfig(
            name=new_name or f"{self.config.name}_clone",
            description=self.config.description,
            resources=ResourceRequirements(**vars(self.config.resources)),
            initial_state=self.config.initial_state.copy(),
            environment=self.config.environment.copy(),
            tags=self.config.tags.copy(),
            metadata=self.config.metadata.copy(),
        )
        
        return Task(new_config)
    
    def get_state(self) -> Dict[str, Any]:
        """获取任务状态"""
        return {
            "task_id": self.task_id,
            "name": self.config.name,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "terminated_at": self.terminated_at.isoformat() if self.terminated_at else None,
            "resources": vars(self.config.resources),
            "event_count": len(self.events),
        }
    
    def save_snapshot(self) -> Dict[str, Any]:
        """保存任务快照"""
        return {
            "task_id": self.task_id,
            "config": {
                "name": self.config.name,
                "description": self.config.description,
                "resources": vars(self.config.resources),
                "initial_state": self.config.initial_state,
                "environment": self.config.environment,
                "tags": self.config.tags,
                "metadata": self.config.metadata,
            },
            "state": self.state.value,
            "timestamps": {
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
                "started_at": self.started_at.isoformat() if self.started_at else None,
                "terminated_at": self.terminated_at.isoformat() if self.terminated_at else None,
            },
            "runtime_data": self.runtime_data,
            "events": [
                {
                    "timestamp": e.timestamp.isoformat(),
                    "event_type": e.event_type,
                    "state_from": e.state_from.value,
                    "state_to": e.state_to.value,
                    "message": e.message,
                }
                for e in self.events
            ]
        }
    
    def _record_event(
        self,
        event_type: str,
        state_from: TaskState,
        state_to: TaskState,
        message: str = ""
    ) -> None:
        """记录事件"""
        event = TaskEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            state_from=state_from,
            state_to=state_to,
            message=message,
        )
        self.events.append(event)


class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
    
    def create_task(self, config: TaskConfig) -> Task:
        """创建任务"""
        task = Task(config)
        self.tasks[task.task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def list_tasks(
        self,
        state: Optional[TaskState] = None,
        tags: Optional[List[str]] = None
    ) -> List[Task]:
        """列出任务"""
        tasks = list(self.tasks.values())
        
        if state:
            tasks = [t for t in tasks if t.state == state]
        
        if tags:
            tasks = [t for t in tasks if any(tag in t.config.tags for tag in tags)]
        
        return tasks
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.destroy()
            del self.tasks[task_id]
            return True
        return False
    
    def archive_completed_tasks(self) -> int:
        """归档已完成的任务"""
        count = 0
        for task in self.tasks.values():
            if task.state == TaskState.TERMINATED:
                if task.archive():
                    count += 1
        return count
    
    def cleanup_destroyed_tasks(self) -> int:
        """清理已销毁的任务"""
        destroyed = [
            task_id for task_id, task in self.tasks.items()
            if task.state == TaskState.DESTROYED
        ]
        for task_id in destroyed:
            del self.tasks[task_id]
        return len(destroyed)


__all__ = [
    "TaskState",
    "TaskTransition",
    "ResourceRequirements",
    "TaskConfig",
    "TaskEvent",
    "Task",
    "TaskManager",
]
