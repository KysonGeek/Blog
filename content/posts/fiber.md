+++
title = "浅谈 React Fiber 架构"
date = 2019-09-12

[taxonomies]
tags = ["FE", "React"]
+++

## What is Fiber ?

“fiber” reconciler 是一个新尝试，致力于解决 stack reconciler 中固有的问题，同时解决一些历史遗留问题。Fiber 从 React 16 开始变成了默认的 reconciler。

<!--more-->

它的主要目标是：

- 能够把可中断的任务切片处理。
- 能够调整优先级，重置并复用任务。
- 能够在父元素与子元素之间交错处理，以支持 React 中的布局。
- 能够在 render()中返回多个元素。
- 更好地支持错误边界。

这里列举 Fiber 的数据结构，仅截取部分重要属性。

```javascript
// A Fiber is work on a Component that needs to be done or was done. There can
// be more than one per component.
export type Fiber = {|
  // These first fields are conceptually members of an Instance. This used to
  // be split into a separate type and intersected with the other Fiber fields,
  // but until Flow fixes its intersection bugs, we've merged them into a
  // single type.

  // An Instance is shared between all versions of a component. We can easily
  // break this out into a separate object to avoid copying so much to the
  // alternate versions of the tree. We put this on a single object for now to
  // minimize the number of objects created during the initial render.

  // Tag identifying the type of fiber.
  tag: WorkTag,

  // Unique identifier of this child.
  key: null | string,

  // The value of element.type which is used to preserve the identity during
  // reconciliation of this child.
  elementType: any,

  // The resolved function/class/ associated with this fiber.
  type: any,

  // The local state associated with this fiber.
  stateNode: any,

  // Conceptual aliases
  // parent : Instance -> return The parent happens to be the same as the
  // return fiber since we've merged the fiber and instance.

  // Remaining fields belong to Fiber

  // The Fiber to return to after finishing processing this one.
  // This is effectively the parent, but there can be multiple parents (two)
  // so this is only the parent of the thing we're currently processing.
  // It is conceptually the same as the return address of a stack frame.
  return: Fiber | null,

  // Singly Linked List Tree Structure.
  // return child sibling 子节点 兄弟节点 这些是将 Fiber tree 连接在一起的重要指针
  child: Fiber | null,
  sibling: Fiber | null,
  index: number,

  // The ref last used to attach this node.
  // I'll avoid adding an owner field for prod and model that as functions.
  ref: null | (((handle: mixed) => void) & { _stringRef: ?string }) | RefObject,

  // Input is the data coming into process this fiber. Arguments. Props.
  pendingProps: any, // This type will be more specific once we overload the tag.
  memoizedProps: any, // The props used to create the output.

  // A queue of state updates and callbacks.
  updateQueue: UpdateQueue<any> | null,

  // The state used to create the output
  memoizedState: any,

  // Dependencies (contexts, events) for this fiber, if it has any
  dependencies: Dependencies | null,

  // Bitfield that describes properties about the fiber and its subtree. E.g.
  // the ConcurrentMode flag indicates whether the subtree should be async-by-
  // default. When a fiber is created, it inherits the mode of its
  // parent. Additional flags can be set at creation time, but after that the
  // value should remain unchanged throughout the fiber's lifetime, particularly
  // before its child fibers are created.
  mode: TypeOfMode,

  // Effect
  // 需要修改的 fiber 上打上这个 tag 来 trace 更新
  // Effect list 是个链表来着 因此有了下面的这些操作
  effectTag: SideEffectTag,

  // Singly linked list fast path to the next fiber with side-effects.
  nextEffect: Fiber | null,

  // The first and last fiber with side-effect within this subtree. This allows
  // us to reuse a slice of the linked list when we reuse the work done within
  // this fiber.
  firstEffect: Fiber | null,
  lastEffect: Fiber | null,

  // Represents a time in the future by which this work should be completed.
  // Does not include work found in its subtree.
  // 用于计算优先级的重要变量
  expirationTime: ExpirationTime,

  // This is used to quickly determine if a subtree has no pending changes.
  childExpirationTime: ExpirationTime,

  // This is a pooled version of a Fiber. Every fiber that gets updated will
  // eventually have a pair. There are cases when we can clean up pairs to save
  // memory if we need to.
  // 版本控制和缓存 用于回滚
  alternate: Fiber | null,
|};
```

![PCD4s6VXUNTMIr5.jpg](https://i.loli.net/2019/09/12/PCD4s6VXUNTMIr5.jpg)

![oepNQ8mZGEyxqnr.jpg](https://i.loli.net/2019/09/12/oepNQ8mZGEyxqnr.jpg)

## setState 内幕

实际上引起 setState 的同步和异步更新的决定性原因是 React 的合成事件机制，它会将合成事件包裹中的 update 放到队列中批量更新，而没有经过合成事件处理的 setState 往往是同步执行的。

![q8jCgx9hSXYtlQy.png](https://i.loli.net/2019/09/12/q8jCgx9hSXYtlQy.png)

## Reference

- [Lin Clark - A Cartoon Intro to Fiber - React Conf 2017 - YouTube](https://youtu.be/ZCuYPiUIONs)
- [GitHub - acdlite/react-fiber-architecture: A description of React’s new core algorithm, React Fiber](https://github.com/acdlite/react-fiber-architecture)
- [Cooperative Scheduling of Background Tasks](https://www.w3.org/TR/requestidlecallback/)
- [window.requestAnimationFrame - Web API 接口参考 | MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/requestAnimationFrame)
- [requestIdleCallback - Web API 接口参考 | MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/requestIdleCallback)
- [React 源码全方位剖析 | 每天一探](http://www.sosout.com/2018/08/12/react-source-analysis.html)
- [React Fiber - 掘金](https://juejin.im/post/5ab7b3a2f265da2378403e57)
- [你真的理解 setState 吗？ - 掘金](https://juejin.im/post/5b45c57c51882519790c7441)
- [【React 深入】React 事件机制-前端外刊评论](https://qianduan.group/posts/5cb1b0e49fd64d5a7458a981)
