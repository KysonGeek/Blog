+++
title = "NestJS 设计模式"
date = 2023-11-29

[taxonomies]
tags = ["NestJS", "Design pattern"]

[extra]
author = { name = "XXXMRG", social= "https://github.com/XXXMrG" }
+++

1. 介绍 NestJS 的基本概念。
2. NestJS 解决了哪些问题。
3. 如何写出不让自己加班的代码。

# 1. NestJS 简介

一个 Node.js 服务端框架，与比较简单的 express 或 koa 不同。

NestJS 提供了更上层的抽象，因此叫它生产级框架更合适，它通过提供大量的设计模式和周边生态，使开发者能够快速地构建大型、复杂的服务端应用。

![nest-level](/imgs/nest/Drawing%202023-11-27%2015.33.42.excalidraw.png)

让我们通过一个简单的代码实例来说明 NestJS 都做了哪些上层的抽象：

下面是一个非常简单的服务端应用，提供了两个接口：

1. 使用原生 Node.js 实现

使用原生 http API，即可以快速的创建一个服务端应用，但注意，代码中需要手动进行路由处理，手动处理响应的 Header, status, body 等每一个细节部分。
可以想象一下，如果我们的服务端应用有 100 个接口，每个接口都需要经过同样的处理逻辑，我们的代码的维护难度将是多么高。

```js
const http = require("http");
const url = require("url");

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const path = parsedUrl.pathname;

  if (path === "/user" && req.method === "GET") {
    // Handle GET request to retrieve user information
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ id: 1, name: "John Doe" }));
  } else if (path === "/user" && req.method === "POST") {
    // Handle POST request to store user information
    let data = "";
    req.on("data", (chunk) => {
      data += chunk;
    });

    req.on("end", () => {
      const user = JSON.parse(data);
      // Store user information
      res.writeHead(201, { "Content-Type": "application/json" });
      res.end(JSON.stringify(user));
    });
  } else {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  }
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

2. 使用 Express 实现：

使用 Express 的实现则清晰很多，中间件机制使得我们不再需要将 request body 的处理逻辑在每个业务路由中都需要重新写一遍，同时我们也不再需要关心响应体构建的每个细节了。我们的代码现在可以比较容易的新增一些接口了，维护难度大大降低！

```js
const express = require("express");
const bodyParser = require("body-parser");

const app = express();
const PORT = 3000;

// use middleware
app.use(bodyParser.json());

app.get("/user", (req, res) => {
  // Handle GET request to retrieve user information
  res.json({ id: 1, name: "John Doe" });
});

app.post("/user", (req, res) => {
  // Handle POST request to store user information
  const user = req.body;
  // Store user information
  res.status(201).json(user);
});

app.use((req, res) => {
  res.status(404).send("Not Found");
});

app.listen(PORT, () => {
  console.log(`Express app listening on port ${PORT}`);
});
```

3. 使用 NestJS 实现：

使用 NestJS 实现的版本，是代码行数最多的版本，并且分散到了好几个文件中！
这看上去，代码没有那么直观了，但好处是，每个模块各司其职，彼此之间的耦合程度更松散了，现在如果你需要开发一个新的接口，你只需要关心你自己的业务逻辑，其他的接口对你来说没有任何影响。

同样新增一个接口，NestJS 的版本一定是对现有代码修改最少的。换句话说，代码的维护难度是最低的！

```ts
// main.ts
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const PORT = 3000;
  await app.listen(PORT);
  console.log(`Nest app listening on port ${PORT}`);
}
bootstrap();

// app.module.ts
import { Module } from "@nestjs/common";
import { UserController } from "./user.controller";
import { UserService } from "./user.service";

@Module({
  controllers: [UserController],
  providers: [UserService],
})
export class AppModule {}

// user.controller.ts
import { Controller, Get, Post, Body } from "@nestjs/common";
import { UserService } from "./user.service";

@Controller("user")
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  getUser() {
    // Handle GET request to retrieve user information
    return this.userService.getUser();
  }

  @Post()
  createUser(@Body() user: any) {
    // Handle POST request to store user information
    return this.userService.createUser(user);
  }
}

// user.service.ts
import { Injectable } from "@nestjs/common";

@Injectable()
export class UserService {
  private user = { id: 1, name: "John Doe" };

  getUser() {
    return this.user;
  }

  createUser(newUser: any) {
    // Store user information
    return newUser;
  }
}
```

| 实现方式  | 特点                               | 抽象层级 | 优点                                                       | 缺点                                               |
| :-------- | :--------------------------------- | :------- | :--------------------------------------------------------- | -------------------------------------------------- |
| 原生 http | 使用原生 API，直接与底层接口交互。 | 低       | 无额外依赖，性能最好                                       | 需要手动处理请求，路由等底层概念，依赖关系难以管理 |
| Express   | 使用了中间件模式，比较轻量         | 中       | 中间件模式使得请求和响应处理起来更加清晰自然               | 构建大型应用时，依赖关系很容易变得混乱             |
| NestJS    | 涉及到的概念多，用于构建大型应用   | 高       | 可以更好的组装代码，模块封装和依赖管理清晰，易于修改和维护 | 涉及概念较多，不易上手                             |

从这些对比我们可以发现，抽象程度越高的框架，开发人员在面对需求变更时要做的修改就越少。

从某种意义上来说，软件架构设计，是一门使得软件更易于变更的艺术。而设计模式，则是开发人员手中的神兵利器。

接下来，让我们一起看看 NestJS 上面那些让人望而生畏的各种概念都解决了哪些问题。

# 2. NestJS 设计模式

自上而下的，我们将了解以下 NestJS 中使用到的设计模式，并简单讲述这些设计模式在 NestJS 中，分别解决了什么问题。

1. 面向对象编程
2. 模块化
3. 依赖注入和控制反转

## 2.1 面向对象编程

面向对象编程（OOP）是老生常谈的编程范式了，在大多数计算机专业的课程中，除了基础的结构化编程外，大家接触最多的就是面向对象编程了。
因此在这里不再过多介绍面向对象编程的一些基础概念了，只为大家抛出一个问题：

面向对象编程的本质是什么？

这里引用架构整洁之道里的一句话：

**面向对象编程对程序控制权的间接转移做出了限制和规范**

让我们详细理解一下这句话：
什么是程序控制权的间接转移？
程序控制权的直接转移非常好理解，就是程序一行一行的执行，按照代码书写的顺序。
那么间接转移呢？前端其实再熟悉不过了，回调函数，事件驱动编程，这都是控制权间接转移的方式。

```js
const fs = require("fs");

fs.readFile("example.txt", "utf-8", (err, data) => {
  if (err) {
    console.error(err);
  } else {
    console.log(data);
  }
});
```

**程序的执行顺序不再是线性的了，而是将控制权转移到了其他的代码块中。**

最原始的程序控制权转移，实际上使用 C 或 CPP 中的函数指针就可以实现了，因此这并不是什么高深的技术。
程序控制权的间接转移是面向对象编程模式的基石，通过对程序控制权的间接转移做出种种限制，面向对象编程才增强了代码的灵活性。

现在回头看一下，在第一小节的三种代码示例里，都使用了什么方式进行程序控制权的间接转移。

1. 原生实现：在处理接口响应时，程序控制权是完全线性的。
2. Express：大量使用了回调函数和中间件
3. NestJS：OOP

接下来，让我们详细看看 NestJS 都使用了面向对象编程中的那些概念，对程序控制权的间接转移都做了哪些限制。

## 2.2 模块化

模块化是 NestJS 中贯彻面向对象编程中「封装」这一基本概念的实现方式，也是 NestJS 组织代码结构的基石。

对于前端开发而言，模块这一概念我们再熟悉不过了（JS 可能是所有编程语言里，模块规范最多的了。。。）

那么为什么 NestJS 还要继续抽象一个 Module 的概念呢？

仔细来看下上面的代码示例中的 app.module.ts，这是应用级别的 module 的配置入口：

```ts
// app.module.ts
import { Module } from "@nestjs/common";
import { UserController } from "./user.controller";
import { UserService } from "./user.service";

@Module({
  controllers: [UserController],
  providers: [UserService],
  // +
  imports: [],
  exports: [],
})
export class AppModule {}
```

在上述代码中，我们可以看到以下内容：

- AppModule 是整个模块的配置中心，也称作依赖注入的容器，它注册了该模块中的所有服务，并且导入和导出了部分服务。
- controllers 负责处理该模块的所有 HTTP 请求。
- providers 负责实现该模块内部的所有业务逻辑细节。
- imports 声明了该模块所使用的外部依赖。
- exports 声明了该模块向外部暴露的服务和接口。

通过这样一个类似配置文件的 module 文件，NestJS 提供了一种清晰、易于维护的依赖关系。当为已有模块添加新功能时，可以保证对其他功能模块的更新没有任何影响。这种模块化的设计使得代码结构更加清晰，便于开发和维护。

模块也是我们接下来要讲的，依赖注入的设计模式中，必不可少的一部分。

## 2.3 依赖注入和控制反转

接下来，我们来看看 NestJS 中最为核心的设计模式：依赖注入和控制反转。

**依赖注入（ID）：**
在 NestJS 中，我们会常常看到下面这样的代码：

```ts
@Injectable()
export class UIBuildService {
  constructor(
    private readonly configService: ConfigService,
    private readonly logger: Logger
  ) {}
}
```

这里有两点与我们常见的 class 不同的地方：

1. 使用了装饰器 `@Injectable`：这个装饰器用于声明一个类是可被其他模块依赖的服务。
2. constructor 的参数中声明了一些 `readonly` 的参数：在 constructor 中，我们可以通过参数的方式声明该模块需要外部注入的依赖模块。

这两个特性结合起来，实现了依赖注入的核心机制。
通过装饰器 `@Injectable` 声明可被注入的服务，并通过 constructor 参数声明依赖模块。
配合我们上面提到的 Module 文件，NestJS 可以自动将依赖注入到对应的地方，使得模块之间的协作更加灵活和可维护。

接下来，让我们来仔细想想，这种设计带来了什么好处。

**控制反转（IOC）：**
假设上面的代码中，`Logger` 和 `ConfigService` 不是通过依赖注入的模块，而只是对这些代码的源码级别的引用，此时，源代码的依赖方向和控制流的方向是一致的：

![flow-normal](/imgs/nest/Drawing%202023-11-28%2019.53.10.excalidraw.png)
控制流决定了我们的源代码必须严格遵守以上依赖关系，无论底层实现的功能模块有多复杂，都必须事无巨细的导入每一个模块，而一旦任何代码出现了变更，上层模块都需要重新编译，重新测试，重新部署。

那么，如果我们使用了依赖注入呢，此时**控制流和源代码的依赖方向就会反转过来。**( 下图中红色实线的部分，源码的依赖方向与控制流的方向相反)
因为有了依赖注入容器，也就是上一节提到的 `Module`，由它负责管理依赖关系，而非通过源码直接依赖：
![flow-reverse](/imgs/nest/Drawing%202023-11-28%2020.07.15.excalidraw.png)
此时，无论 `Logger` 模块内部如何变更，只要拥有稳定的统一抽象层（在这里是依赖注入容器，在其他语言中，可能是接口），`Controller` 都不会收到任何影响，它不需要被重新编译，重新部署，内部的控制流也不需要重新再测试一遍。

**A 不想被 B 的修改影响，那么就让 B 依赖 A，而不是 A 依赖 B。**

高层逻辑依赖底层实现，变成底层实现依赖高层逻辑约定的接口。

这样的设计能够带来什么好处？

高层逻辑往往是不会经常变更的，而底层实现是代码中比较复杂，容易出问题，经常需要变更的地方，我们不希望这些地方的修改会对高层逻辑有任何影响。

同时，我们更不希望两个功能不相关的底层实现模块在代码上存在任何耦合的地方。

回头看控制反转后的依赖关系图，此时如果我们希望替换一个底层的 `Logger` 实现，是不是只需要变更 `LoggerService` 自己就可以了，增加和删除一个底层实现模块也是同样的

**在可维护性较好的架构中，实现一个新的需求时，往往只需要新增代码，而不需要修改任何现有的代码。**

这能够大大减少开发人员和测试人员的工作量，我们再也不用加班了！！！

# 3. 如何实现一个依赖注入容器

在上面的 NestJS 代码中，我们看到了很多平时不会用到的 TS 语法，因此纯粹出于好奇，让我们在这一小节一起看一下，实现一个 NestJS 的依赖注入容器，需要分几步？

1. 先不看装饰器，依赖注入容器其实就是一个 Map
2. 背后依赖了反射机制，来更加动态控制模块的实例创建过程
3. 装饰器是语法糖，也是其他语言中实现依赖注入框架时的代码风格。能够提供清晰简洁的 API。

**一个简单的依赖注入容器实际就是个 Map：**

```ts
class DependencyContainer {
  private dependencies: Map<string, any> = new Map();

  // 注册提供者
  registerProvider(identifier: string, provider: any): void {
    this.dependencies.set(identifier, provider);
  }

  // 解析依赖项
  resolve(identifier: string): any {
    if (!this.dependencies.has(identifier)) {
      throw new Error(`Dependency not registered: ${identifier}`);
    }

    return this.dependencies.get(identifier);
  }
}

// 示例：定义服务类
class CatService {
  getHello(): string {
    return "Meow!";
  }
}

// 示例：使用依赖注入容器
const container = new DependencyContainer();

// 注册提供者
container.registerProvider("CatService", CatService);

// 解析依赖项
const catServiceInstance = new (container.resolve("CatService"))();
console.log(catServiceInstance.getHello()); // 输出: Meow!
```

我们不知不觉的实现了一个最简单的依赖注入容器，它可以向容器内注册新的依赖模块，并根据需要，动态的实例化这些依赖。

接下来，我们来实现依赖注入容器最重要的功能，自动解析模块间的依赖关系，并实现依赖注入。

**依靠反射来实现依赖的自动注入：**

我们又接触到了一个新的设计模式：反射。这是一个在 Javascript 中不常见的设计模式，更多的出现在 Java 编程中。

**反射是一种在运行时获取和操作程序元信息的能力。**

- 什么是程序元信息？
  - 对于面向对象编程而言，对象的属性，方法，构造函数，这些都是程序的元信息(metadata)。
- 为什么要在运行时获取？
  - 看我们上面的依赖注入示例，模块之间的依赖关系并不是通过源码依赖关系直接声明的，我们需要在程序的运行阶段，动态的获取依赖关系。
  - 动态实例化，模块的实例创建过程可能是动态的。比如某些模块我们希望全局单例，有些模块我们希望在每次请求处理时，都新建一个全新的实例。这些创建策略是通过配置的方式声明的，因此都需要在运行时获取，而非在编译阶段。

在 Javascript 中，我们一般使用 [reflect-metadata](https://github.com/rbuckton/reflect-metadata) 来实现上述能力。
直接来看一个实例：

```ts
import "reflect-metadata";

class DependencyContainer {
  private dependencies: Map<string, any> = new Map();

  // 注册提供者
  registerProvider(identifier: string, provider: any): void {
    this.dependencies.set(identifier, provider);
  }

  // 解析依赖项
  resolve<T>(identifier: string): T {
    if (!this.dependencies.has(identifier)) {
      throw new Error(`Dependency not registered: ${identifier}`);
    }

    const provider = this.dependencies.get(identifier);
    const paramTypes = Reflect.getMetadata("design:paramtypes", provider) || [];
    const params = paramTypes.map((type: any) => this.resolve(type.name));
    return new provider(...params);
  }
}

// 示例：定义服务类
class CatService {
  getHello(): string {
    return "Meow!";
  }
}

// 示例：定义控制器类
class CatController {
  private readonly catService: CatService;

  constructor(catService: CatService) {
    this.catService = catService;
  }

  getHello(): string {
    return this.catService.getHello();
  }
}

// 使用 reflect-metadata 注册参数类型
Reflect.defineMetadata("design:paramtypes", [CatService], CatController);

// 示例：使用依赖注入容器
const container = new DependencyContainer();

// 注册提供者
container.registerProvider("CatService", CatService);

// 解析依赖项
const catControllerInstance = container.resolve<CatController>("CatController");
console.log(catControllerInstance.getHello()); // 输出: Meow!
```

注意这一行：

```ts
// 使用 reflect-metadata 注册参数类型
Reflect.defineMetadata("design:paramtypes", [CatService], CatController);
```

这里我们使用了 Reflect 来声明了一个 metadata，保存了 `CatController` 依赖的模块，这里的数据与 `CatController` 动态地绑定在了一起。
这样一来，在创建 `CatController` 的实例的时候，就可以访问到它的依赖模块，并将其注入在 `CatController` 中。

这样确实可以实现依赖注入，但是每次都需要使用 `defineMeta`，看起来有点不够自动化和优雅。

我们希望能够更优雅地访问注册在类构造函数中的依赖关系。装饰器就是用来解决这个问题的。

**装饰器不过就是语法糖：**

我们知道，JS 和 TS 的装饰器有些不同，但本质上就是一些函数。我们先来复习一下：

1. JS：可以应用于类、方法、属性等。
   1. 类装饰器：第一个参数是类本身，第二个参数是上下文
2. TS：支持应用于类、方法、属性、参数等
   1. 参数装饰器，接收以下参数：
      1. 类的构造函数或原型
      2. 参数名
      3. 参数的索引

因为 JS 与 TS 的装饰器支持的能力有些差别，因此在 NestJS 中，二者在开发模式上也有一些区别：

使用 JS 时，依赖注入需要这样声明：

```js
@Controller()
@Dependencies(AppService)
export class AppController {
  constructor(appService) {
    this.appService = appService;
  }

  @Get()
  getHello() {
    return this.appService.getHello();
  }
}
```

而 TS 只需要声明在构造函数的参数中，更加清晰直观：

```ts
@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}
```

因为 TS 的参数装饰器，可以直接在运行时获取参数的信息，此时我们只需将上面 `defineMetaData` 的逻辑直接放在一个参数装饰器中即可。

```ts
// 装饰器用于标记依赖注入
function Inject(identifier: string): ParameterDecorator {
  return (
    target: Object,
    propertyKey: string | symbol,
    parameterIndex: number
  ) => {
    const existingInjects = Reflect.getMetadata("design:injects", target) || [];
    existingInjects.push({ parameterIndex, identifier });
    Reflect.defineMetadata("design:injects", existingInjects, target);
  };
}

class CatController {
  private readonly catService: CatService;

  // 依赖注入通过装饰器标记
  constructor(@Inject("CatService") catService: CatService) {
    this.catService = catService;
  }

  getHello(): string {
    return this.catService.getHello();
  }
}
```

# 5. 反模式

1. 不清晰的模块划分 -> 正确使用模块

```ts
// 错误的模块划分, AnimalService 同时为两个 Controller 提供接口
@Module({
  controllers: [CatController, DogController],
  providers: [AnimalService],
})
export class AppModule {}

// 正确的模块划分
@Module({
  imports: [CatsModule, DogsModule],
})
export class AppModule {}
```

2. 所有逻辑都写在 Controller 中 -> 单一指责

```ts
// 控制器中包含所有逻辑
@Controller("cats")
export class CatController {
  constructor() {}

  @Get()
  getAllCats(): string {
    // 处理逻辑...
    return "All cats";
  }

  @Post()
  createCat(@Body() cat: CreateCatDto): string {
    // 处理逻辑...
    return "Cat created";
  }
}

// 拆分逻辑到服务中
@Controller("cats")
export class CatController {
  constructor(private readonly catService: CatService) {}

  @Get()
  getAllCats(): string {
    return this.catService.getAllCats();
  }

  @Post()
  createCat(@Body() cat: CreateCatDto): string {
    return this.catService.createCat(cat);
  }
}

// 单一职责的服务
@Injectable()
export class CatService {
  getAllCats(): string {
    // 获取所有猫的逻辑...
    return "All cats";
  }

  createCat(cat: CreateCatDto): void {
    // 创建猫的逻辑...
  }
}
```

3. 直接依赖实现，而不是依赖接口 -> 违反控制反转

```ts
// 依赖实现
import { CatService } from "./catSerivce";
@Controller("cats")
export class CatController {
  constructor() {
    this.catService = new CatService();
  }
}

// 依赖接口
@Controller("cats")
export class CatController {
  constructor(private readonly catService: CatService) {}

  // ...
}
```

# 思考

1. 为什么依赖注入这种设计模式，在前端应用中很少出现，而在服务端框架中却被业界广泛使用？
   1. 当然 Angular 是个例外，但也不妨想想，为什么老外那么喜欢用 Angular，国内却基本无人问津？
2. 前端开发时，往往使用哪些设计模式来面对频繁的变更？

## 参考

推荐阅读：

1. 架构整洁之道
2. [设计模式与 Typescript](https://refactoringguru.cn/design-patterns/typescript)
3. [Proposal](https://rbuckton.github.io/reflect-metadata/)
