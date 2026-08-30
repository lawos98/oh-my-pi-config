---
name: kotlin-intellij-plugin-dev
description: JetBrains IntelliJ Platform plugin development in Kotlin. Use when creating plugin actions, services, tool windows, file editors, extension points, or working with IntelliJ SDK APIs. Covers plugin.xml registration, PSI tree, VFS, Document model, AnAction lifecycle, and project/application services. Triggers - intellij plugin, jetbrains plugin, plugin.xml, AnAction, tool window, file editor, PSI, VFS listener, extension point, service registration.
---

# Kotlin IntelliJ Plugin Development

You are an expert IntelliJ Platform plugin developer. Apply these conventions when writing or reviewing JetBrains plugin code.

## Architecture Rules

### Services
- `@Service(Service.Level.PROJECT)` for project-scoped state
- `@Service(Service.Level.APP)` for application-wide singletons
- Access: `project.service<MyService>()` or `service<MyService>()`
- Implement `Disposable` for cleanup; register children via `Disposer.register(parentDisposable, child)`

### Actions
- Extend `AnAction` for toolbar/menu/context-menu items
- Override `actionPerformed(e: AnActionEvent)` for execution
- Override `update(e: AnActionEvent)` for dynamic enable/disable
- Get project: `e.project ?: return`
- Register in `plugin.xml` under `<actions>` with keyboard shortcuts

### File Editors (Editor Tabs)
- Triple pattern: `VirtualFile` + `FileEditor` + `FileEditorProvider`
- VirtualFile: extend `LightVirtualFile`, override `isWritable`, `getFileType`
- FileEditor: implement `FileEditor`, return component via `getComponent()`
- Provider: implement `FileEditorProvider`, check `accept(file)` for your VirtualFile type
- Open tab: `FileEditorManager.getInstance(project).openFile(virtualFile, true)`

### Tool Windows
- Implement `ToolWindowFactory`, register in plugin.xml
- Use `createToolWindowContent(project, toolWindow)` to add UI
- Anchor: left, right, bottom

### Plugin.xml
- Declare `<depends>` for required platform modules
- Use `<extensions defaultExtensionNs="com.intellij">` for extension points
- Optional dependencies via separate XML files + `<depends optional="true" config-file="...">`

## Threading Rules

- **EDT (UI Thread)**: All UI operations, document writes via `WriteCommandAction`
- **Background**: Long-running tasks via `ProgressManager.getInstance().run(Task.Backgroundable(...))`
- **Read Action**: `ReadAction.compute { }` for PSI/index access from background
- **Write Action**: `WriteCommandAction.runWriteCommandAction(project) { }` for document/PSI modifications
- Never block EDT. Never access PSI without read lock from background.

## Common Patterns

### Notifications
```kotlin
NotificationGroupManager.getInstance()
    .getNotificationGroup("My Group")
    .createNotification(message, NotificationType.INFORMATION)
    .notify(project)
```

### Listeners
```kotlin
project.messageBus.connect(disposable).subscribe(TOPIC, listener)
```

### VFS Operations
```kotlin
LocalFileSystem.getInstance().refreshAndFindFileByPath(path)
VirtualFileManager.getInstance().addVirtualFileListener(listener, disposable)
```

### Settings (Persistent State)
```kotlin
@State(name = "MySettings", storages = [Storage("myPlugin.xml")])
class MySettings : PersistentStateComponent<MySettings.State> { ... }
```

## Anti-Patterns (BLOCKED)
- ❌ `@Suppress("UNCHECKED_CAST")` — fix the type safety
- ❌ Blocking EDT with `Thread.sleep()` or synchronous I/O
- ❌ Accessing PSI from background without ReadAction
- ❌ Using deprecated `createLocalShellWidget` — use `createShellWidget` or new Terminal API
- ❌ Hardcoding paths — use `PathManager`, project basePath, or settings
- ❌ Ignoring `Disposable` lifecycle — always register disposables properly
