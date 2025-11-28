+++
title = "类型系统入门"
date = 2024-03-05

[taxonomies]
tags = ["Type System", "TypeScript"]

[extra]
author = { name = "XXXMRG", social= "https://github.com/XXXMrG" }
+++

1. 简单介绍类型系统的概念。
2. 讲述类型系统的应用。
3. 类型系统在 Typescript 和 Rust 中的应用。

本文 idea 来自： [https://suica.github.io/write-you-a-typescript](https://suica.github.io/write-you-a-typescript) 借鉴了很多其中的示例和思想。

# 1. 类型系统简介

## 1.1 什么是类型系统

举个例子，参考自： [https://suica.github.io/write-you-a-typescript](https://suica.github.io/write-you-a-typescript)

> 例 1：997 是一个质数。

> 例 2：997 是一个跑。

如果我们来判断这句话第二句话是否正确，我们可以立刻下结论——它是错的——而不用去理解这个命题涉及的任何数学概念。因为这句话在**语法**上就是错的。这其实就是一种类型检查。

以下是两个比较严谨的类型系统定义：

> 在计算机科学中，类型系统用于定义如何将编程语言中的数值和表达式归类为许多不同的类型，以及如何操作这些类型，还有这些类型如何互相作用。
> 类型可以确认一个值或者一组值具有特定的意义和目的。
> [https://en.wikipedia.org/wiki/Type_system](https://en.wikipedia.org/wiki/Type_system)

类型系统是一种可行的、基于语法的技术，它根据值的种类对词组进行分类，从而证明程序不会有某些行为。（From Types and Programming Languages）

- 类型赋予意义。（限制某些操作）
- 类型是对底层内存布局的一个抽象。（不同的类型，会有不同的内存布局和内存分配的策略。）
- 类型是写给编译器看的注释。（类型由编译器能够分析的规则组成）

## 1.2 类型系统的作用

**验证软件的正确性**

不需要执行程序代码，就能够检查代码中的错误。

**提供抽象机制**

```ts
type User = {
  id: number;
  name: string;
  email: string;
};

function getUser(id: number): User {
  // Fetch user from database
}
```

将现实世界中的实体，抽象成编程语言中的类 / 接口，这是面向对象编程领域中的经典方法。

将无意义的数据抽象成有实际意义的接口的过程，离不开类型系统。

**类型提供文档能力**

良好的 TS 代码不需要过多自然语言的注释，类型系统是代码的自我文档化的工具。

```ts
type Numeric = number | string;

// 当传入字符串时，返回字符串数组
// 当传入 number 时，返回 number
function parseInput<T extends Numeric>(
  input: T
): T extends string ? string[] : number {}

const result1 = parseInput("123"); // 类型推断为 string[]
const result2 = parseInput(123); // 类型推断为 number
```

**类型系统不能做什么？**

类型是轻量化的形式化证明方法（formal method）。

形式化证明是计算机科学领域，理论性非常强的一门学科，它旨在通过严谨的数学方法验证软件属性。

用数学方式描述程序的行为，数学公式是可证明的，故程序的行为是可证明的。

一般用在对系统的稳定性有极高要求的行业中，如：

- NASA 的火箭发射系统。
- 核设施的电子控制系统。
- 金融交易系统。
- 等等......

形式化证明可以验证，但类型系统通常不能验证的内容：

- 逻辑正确性
- 算法的性能
- 安全性
- 并发问题

某些类型系统的设计能一定程度上避免安全和并发问题，但类型系统不是能够严谨地验证这些问题的工具。

## 1.3 类型系统的地位

类型论(Type Theory, TT)是类型系统背后的理论。

类型论是指导编程语言设计的关键角色，是现代编程语言中，数据类型、类型系统、编译器设计的理论基础。

**举个比较典型的应用示例：**

类型检查(Type Checking)在经典的编译流程中，属于语义分析的一部分。
编译器会在此阶段利用类型系统，完成以下任务：

- 类型检查
- 变量绑定
- 作用域检查，变量遮蔽
- 类型擦除

**在计算机理论科学领域：**

类型论与形式化方法密切相关，关联【程序语言】和【推理系统】是计算机理论科学和数学领域中经久不衰的话题。（参见：[柯里-霍华德(Curry-Howard)同构](https://zh.wikipedia.org/zh-cn/%E6%9F%AF%E9%87%8C-%E9%9C%8D%E5%8D%8E%E5%BE%B7%E5%90%8C%E6%9E%84)

# 2. 类型系统基础

这一小节主要描述，如何利用数学和逻辑学的工具，来严谨的描述类型系统，内容偏理论，遇到不理解的概念可参考后面的案例理解。

## 2.1 类型系统的组成

一般来说，一个最简单的类型系统，由以下三部分组成：

- 类型
- 规则
- 定型环境

### 2.1.1 类型

一些基本的数据类型，如数字，字符串，函数等。

与编程语言中的类型不同，因为类型系统是【描述编程语言的另一种语言（一般称为元语言 meta language）】，所以这里不会使用与编程语言中的类型中相同的符号来代表同一类型。

在数学上，一般会使用的集合中的【关系】来描述两个或 N 个集合之间的关系，类型实际上可以简单的看做一种集合。

比如我们说 123 是一个 Number 类型，实际上是在描述 123 是 Number 集合的一个子集。
在类型系统一般写作： `123: Num`

### 2.1.2 规则

有了基本类型，根据基本类型推演出表达式的类型的过程，叫做推演规则。

描述推演规则的工具，叫做自然推演，这是一种在逻辑学中广泛应用的工具，用于直观的描述人类自然的推理方式。

举个例子，同样参考自 [https://suica.github.io/write-you-a-typescript](https://suica.github.io/write-you-a-typescript)：

对于二元的加法`+`来说，我们有：

$$
{x: \mathbf{Num},\ y: \mathbf{Num} \over x + y : \mathbf{Num} }\ (\text{N-Add})
$$

- 每个推演规则，都由横线上下分割。
- 在横线之上的，是使用这条规则的前提；横线之下的，是在前提满足的情况下，使用这条规则能得到的结论。
- 横线右边的，是出于便于讨论的目的，给这条规则取的名字。这条规则叫做`N-Add`。

`N-Add`这个规则的意思是说：若`x`的类型是`Num`，`y`的类型是`Num`，那么`x+y`也是`Num`。

这种写法，叫做**自然推演**(Natural Deduction)。

对于复杂的表达式，自然推演表达式可能会以树状结构不断扩张，这颗树叫做导出树，**类型检查，就是隐式地构造这棵导出树，或者检查这个导出树是否正确**。

### 2.1.3 定型环境

回过头来看上面定义的规则，该规则定义了两个 `Num` 类型的值相加，得到的表达式的类型仍为 `Num`，但它其实并未定义什么类型才是 `Num`。
这个类型的定义是与编程语言的语法有关的。

在特定的编程语言中，`Num` 可以有不同的表达形式，在 Javascript 中，我们可以使用 AST 中的表达式类型来表示，`Num` 类型就是一个 `NumericLiteral` 数字字面量。

定义基本类型很简单，但定义函数类型就不那么容易了。
函数类型，其特殊之处在于，只有对函数的入参和返回值的细节进行描述，类型规则才是有意义的。

考虑这个简单的函数例子：`(x: Num) => x + 1`
在这个例子中，我们标记了参数类型 `x: Num`，但在推断返回值 `x + 1` 的类型的时候，我们实际上并不知道 `x` 的类型，因为这个表达式上并没有类型标注。
即使是静态类型语言，我们也只需要定义一次变量的类型，而不需要在每个表达式中重新标注变量的类型。

我们需要教给类型系统使用类型标注的方法，这个方法就是定型环境。
可以把定型环境想象成一个列表，列表中维护了我们标记的，变量和类型的对应关系。
通常情况下，我们会使用 \\( \Gamma \\) (Gamma)符号来表示定型环境。

### 2.1.4 总结

这一小节中简单讲述了类型系统在数学或逻辑学上的组成定义。
上面提到的工具，实际上都为了一个目标服务，那就是将类型系统进行数学建模。

在数学建模后，类型系统中的很多问题都可以用数学的方法去解答，有一些例子可以参考：

- 在某些类型系统中，类型推导问题可以转化为一种形式的线性方程组。
- Hindley-Milner 类型推断算法，一种广泛应用的类型推导算法，通过收集并解决约束来推导类型。

## 2.2 类型系统的分类

类型系统可以按照多个不同的标准进行分类，这里讲几个比较常见的分类：

- 静态类型 / 动态类型
- 名义类型 / 结构类型
- 强类型 / 弱类型

### 2.2.1 动态类型系统

常见的使用动态类型系统的编程语言：

- Python
- Ruby
- JavaScript

变量的类型是由运行时的解释器来动态标记的，这样就可以动态地和底层的计算机指令或内存布局对应起来。

举个例子，下面是 v8 运行时里，加法的[具体实现](https://github.com/v8/v8/blob/e300c7a113030ef0e15fc7bcbe211a1dbeabf9d6/src/objects/objects.cc#L919)：

```cpp
MaybeHandle<Object> Object::Add(Isolate* isolate, Handle<Object> lhs,
                                Handle<Object> rhs) {
  // 两边都是 number ，直接加起来
  if (IsNumber(*lhs) && IsNumber(*rhs)) {
    return isolate->factory()->NewNumber(Object::Number(*lhs) +
                                         Object::Number(*rhs));
  } else if (IsString(*lhs) && IsString(*rhs)) {
    // 两边都是字符串，直接连接起来
    return isolate->factory()->NewConsString(Handle<String>::cast(lhs),
                                             Handle<String>::cast(rhs));
  }

  // 检查是否均为基本类型
  ASSIGN_RETURN_ON_EXCEPTION(isolate, lhs, Object::ToPrimitive(isolate, lhs),
                             Object);
  ASSIGN_RETURN_ON_EXCEPTION(isolate, rhs, Object::ToPrimitive(isolate, rhs),
                             Object);

  // 如果有一个是字符串，则尝试转成字符串相连接
  if (IsString(*lhs) || IsString(*rhs)) {
    ASSIGN_RETURN_ON_EXCEPTION(isolate, rhs, Object::ToString(isolate, rhs),
                               Object);
    ASSIGN_RETURN_ON_EXCEPTION(isolate, lhs, Object::ToString(isolate, lhs),
                               Object);
    return isolate->factory()->NewConsString(Handle<String>::cast(lhs),
                                             Handle<String>::cast(rhs));
  }

  // 最后尝试把两边都转成数字，然后相加
  ASSIGN_RETURN_ON_EXCEPTION(isolate, rhs, Object::ToNumber(isolate, rhs),
                             Object);
  ASSIGN_RETURN_ON_EXCEPTION(isolate, lhs, Object::ToNumber(isolate, lhs),
                             Object);
  return isolate->factory()->NewNumber(Object::Number(*lhs) +
                                       Object::Number(*rhs));
}
```

可以看到简单的加法运算中，v8 都需要对左右操作数进行详尽的类型检查，来兼容各种可能情况。

### 2.2.2 静态类型系统

常见的使用静态类型系统的编程语言：

- C++
- Java
- Rust

变量和表达式的类型是由编译时确定的，类型检查在程序运行前就已经完成，有机会更高效的利用内存布局。

举一个 CPP 中的例子：

```cpp
class Example {
	char a; // 1 字节
	int b; // 4 字节
	char c; // 1 字节
};
```

在 CPP 中，上述类的实际内存占用往往不是 1 + 4 + 1 = 6 字节。
为了保证类的内存布局是类成员中最大的成员的倍数，char a 和 char b 会被填充至 4 字节，因此这个类实际会占用 12 字节。

> 将内存对齐，会提升内存访问的效率，因为计算机的数据总线往往有固定的宽度，如 32 位（4 字节），64 位（8 字节），CPU 每次读取数据是按照数据总线的宽度来的，如果数据是按照宽度对齐的，那么 CPU 只需一次即可读入这个数据。

### 2.2.3 名义类型 / 结构类型

名义类型和结构类型主要是从类型的兼容性角度来区分的。

在名义类型系统中，判断两个类型是否兼容 / 等价，只与其声明有关，与类型的结构没关系。

即使是两个结构完全相同的 Java class，只要二者不具有父子类型关系，这两个类型就是不兼容的。
还是以 CPP 举例：

```cpp
class Example {
    char a;
    int b;
    char c;
};

class ExampleB {
    char a;
    int b;
    char c;
};

bool Foo(Example e) {
    // 函数实现...
    return true;
}

int main() {
    Example exampleObj;
    ExampleB exampleBObj;

    Foo(exampleObj);  // 这是有效的，因为exampleObj是Example类型的实例
    Foo(exampleBObj);  // 这是无效的，即使ExampleB的结构与Example相同，但它们是不同的类型
    return 0;
}

```

使用名义类型的语言：

- Java
- C++

结构类型大家就比较熟悉了，只要两个类型的结构完全相同，这两个类型就是等价的。
上面的例子如果用 Typescript 重写，不论使用 `Example` 还是 `ExampleB` 都可以正常调用 `Foo` 函数。

使用结构类型的语言：

- Typescript
- Go

### 2.2.4 强 / 弱类型

强 / 弱类型系统是纯主观的概念，没有任何理论依据。

比如对于 C 语言，有人认为他是强类型的，因为它是静态类型的。
也有人认为他是弱类型的，因为它允许隐式类型转换。

# 3. 类型系统的应用

## 3.1 泛型

泛型实际上是一种参数多态（Polymorphism）

在面向对象编程中，多态是非常重要的一个概念，其意义在于，赋予同一份代码多种行为。
对应到类型系统中，泛型的本质就是赋予同一份代码多种类型。

这使得程序员在使用泛型开发时，不需要关心数据类型，只关心数据结构。

不同的编程语言在实现泛型特性时，可能采用完全不同的处理方式，具体我们会在后面的案例中展开讨论。

## 3.2 Typescript 的类型系统

上面提到，Typescript 使用了结构化类型系统。

除此之外，Typescript 最被人津津乐道的，就是其作为类型系统，却能够被证明是图灵完备的。

图灵完备是指，一门编程语言可以表达所有可以计算的问题，这在编程语言设计中很容易实现，但在类型系统设计时则少有提及。

这足以证明 Typescript 的复杂程度，这里我们主要来看看以下四点 Typescript 特性，并将其与编程语言中的概念相关联。

**条件类型：**
条件类型可以根据类型之间的关系进行选择，这有点像编程语言中的 `if-else` 分支结构。

```ts
type IsNumber<T> = T extends number ? "Yes" : "No";

type Result1 = IsNumber<number>; // "Yes"
type Result2 = IsNumber<string>; // "No"
```

**映射类型：**
映射类型可以根据既有的类型创建新类型，在有些时候，这类似于循环或映射操作。

```ts
type ReadOnly<T> = {
  readonly [P in keyof T]: T[P];
};

type Original = { a: number; b: string };
type Modified = ReadOnly<Original>;
```

在这里，`ReadOnly` 将 `Original` 类型的所有属性都变为只读属性。

**递归类型:**

TypeScript 支持递归类型定义，即类型可以直接或间接引用自身。这使得类型系统能够表达复杂的数据结构，如树或链表。

```ts
type TreeNode<T> = {
  value: T;
  left: TreeNode<T> | null;
  right: TreeNode<T> | null;
};

const tree: TreeNode<number> = {
  value: 1,
  left: { value: 2, left: null, right: null },
  right: { value: 3, left: null, right: null },
};
```

这个示例定义了一个简单的二叉树节点类型。

**高阶类型：**

通过一些技巧，可以在 Typescript 模拟高阶类型，这类似于其他函数式编程语言中的高阶函数。

```ts
type Box<T> = { value: T };
type BoxedProperty<T, K extends keyof T> = {
  [P in K]: Box<T[P]>;
};

type Original = { a: number; b: string };
type Boxed = BoxedProperty<Original, "a" | "b">;
```

在这个示例中，`BoxedProperty` 类型对 `Original` 类型中的指定属性进行“装箱”。

**more:**

想了解 Typescript 还能实现哪些酷炫的东西？

参考：

- [用 TypeScript 类型运算实现一个中国象棋程序](https://zhuanlan.zhihu.com/p/426966480)
- 类型体操：[https://github.com/type-challenges/type-challenges](https://github.com/type-challenges/type-challenges)

## 3.3 Rust 的类型系统

提到 Rust 的类型系统，离不开的就是其非常严格的所有权和生命周期机制。
这些机制从语法和编译器的层面上，为 Rust 提供了非常强大的内存安全保证，并且不需要垃圾回收。

我们今天主要讲两点：

1. 所有权和 Affine type（仿射类型）
2. Rust 是如何实现泛型的

### 3.3.1 所有权

所有权是 Rust 中最独特的特性之一，它基于以下几个规则：

1. **每个值在 Rust 中都有一个称为其“所有者”的变量。**
2. **任何时候，值只能有一个所有者。**
3. **当所有者离开作用域，其值将被丢弃。**

这其实是建立在 Rust 使用的类型系统 -> Affine type（仿射类型）之上的。

仿射类型，可以看作是一种更宽松的线性类型系统。
线性类型系统具有我们上面第二节中所提到的，所有其他类型系统都不具备的限制规则。

在线性类型系统中：

1. 每一个值，都只能被使用一次。
2. 值不能够随意复制或丢弃。
3. 外部资源强制释放。

如果对并发或系统编程有一定了解，我们会发现，如果我们的代码都能够严格按照线性类型系统的限制开发，那么**并发问题几乎是不可能存在的。**

但线性类型系统的限制太严格了，以至于截至目前，完全使用线性类型系统的生产级别的编程语言还没有出现。

仿射类型则是线性类型系统目前最显著的应用场景，Rust 通过引入所有权的概念，将很大一部分限制从语法层面，转移到了编译器层面去实现，这很好的平衡了研发效率和安全性，这也是 Rust 在系统编程领域中迅速崛起的主要原因。

Rust 的仿射类型主要修改了以下限制：

1. 值不是只能使用一次，而是只能被一个“所有者“拥有。
2. 其他”人“可以向”所有者“借用值，而不直接获得其所有权。但借用有限制。
   1. **不可变借用：** 允许读取数据但不能修改。可以同时有任意个。
   2. **可变借用：** 允许改变数据，但在同一时刻只能有一个可变借用。

### 3.2.2 Rust 的泛型

我们知道，Typescript 中，泛型并不会改变函数的最终实现，在经过 tsc 编译后，声明的所有类型都将被擦除，因此函数的实现中，我们仍需要针对各种可能的参数类型分别处理。

在 Rust 中则不然，我们知道，Rust 是静态类型的，意味着即使是使用了泛型，Rust 的编译器也必须在编译阶段就明确函数的参数的类型，这需要编译器对泛型函数做额外的处理。

想象一下，对于以下泛型函数，在静态类型系统中该如何实现：

```rust
// 定义一个泛型函数，它接受一个类型为 T 的参数
fn example<T>(arg: T) {
    // 函数体，这里只是打印出了参数的一些信息
    println!("Processing a value of type: {}", std::any::type_name::<T>());
}

fn main() {
    // 调用泛型函数，传入一个整数
    example(42);

    // 调用相同的泛型函数，但传入一个字符串切片
    example("Hello, world!");
}
```

**泛型“单态化”（Monomorphization）：**

单态化的过程其实很好理解，既然不能在运行时判断类型，那么就针对所有用到了泛型函数的地方，为其在编译时单独实例化一个函数单纯处理其类型。

在上面的例子中，编译后的代码中会有两个版本的 example 函数，一个参数类型是 int 类型，另一个是字符串切片类型。

这样的实现可以保证 Rust 的泛型函数在执行时没有任何性能损耗，实例化后的函数跟普通的函数没有任何区别，可以享受编译器对函数的所有优化策略。

但这样实现实际上有一个很显著的缺陷，当泛型函数很多时，代码占用的内存会显著增多。

这个问题在 Rust 中可以通过特型对象指针（本质上是一个胖指针，超出本文讨论范畴，大家自行探索）的方式来解决，但在现代系统编程的实际场景下，内存资源几乎不会有这么紧张的情况，所以能用泛型的情况还是推荐用泛型，可以拥有更好的性能和安全性。

## 5. 总结

类型系统跟形式化证明一样：

- 都是将编程语言中的类型 / 语法，转换成非常严谨的数学定义。
- 利用数学公式，公式是可证明的。
- 从而可以推断得到类型 / 逻辑也是可以被证明的。

类型系统是【逻辑学】和【数学】在计算机领域的典型应用之一，无论是计算机偏理论的学科领域还是实际的应用领域都有涉及，希望大家能通过本文入门类型系统！

**思考：**

其实以其类型系统强大著称的语言不是 TS 也不是 Rust，而是 **Haskell** 和 **Scala** ，大家可以自行了解。

**参考资料：**

1. [https://suica.github.io/write-you-a-typescript](https://suica.github.io/write-you-a-typescript)
2. [https://www.amazon.com/dp/0262162091](https://www.amazon.com/dp/0262162091)
3. [https://langdev.stackexchange.com/questions/2692/how-should-i-read-type-system-notation](https://langdev.stackexchange.com/questions/2692/how-should-i-read-type-system-notation)
