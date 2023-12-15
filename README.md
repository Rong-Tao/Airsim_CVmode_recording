# 日志 - Debugging and Progress Tracking

## 目标：实现 UE5 + AirSim 的无缝运行

由于调试过程中遇到不少问题，特此记录以便追踪解决方案。

## 目前环境和工作流

我们的目标是在 UE5 中成功运行 AirSim。传统的组合是 UE4 + AirSim，但由于官方版本不支持 UE4.27 及更高版本，我们选择在 UE5 中尝试。当前使用的 AirSim 版本来自于两个 GitHub 上的 fork：

- [Colossem](https://github.com/CodexLabsLLC/Colosseum)
- [czero69](https://github.com/czero69/AirSim)

Colosseum Main目前支持到 UE5.2,如果想要尝试其他版本的去翻看别的branch，而 czero69 尚未进行测试。

## 问题以及解决方式

1. **按 R 录像文件是黑的**
   - 这个问题已在 [GitHub issue](https://github.com/CodexLabsLLC/Colosseum/issues/65) 中得到解决。实际上，问题是将 RGBA 图像中的 A（Alpha）删除。

2. **使用 Python 录像文件是纯白的**
   - 这个问题主要涉及光影，目前尚不清楚如何调整到合适的位置。
   - 大致原理是：UE 具有自动眼部适应功能，因此您可能会看到纯白画面，然后慢慢眼球适应。在 [关闭眼部适应](https://www.youtube.com/watch?v=0etGOh-USrQ&t=91s&ab_channel=WorldofLevelDesign) 后，光线的调整仍然是一个问题，但有两个可调节的方面：
      + Post processing shader
      + 光源亮度

3. **主视角图像和 AirSim 录制图像不符合 !!!(最大的问题)**
   - [示意图](https://github.com/CodexLabsLLC/Colosseum/issues/65#issuecomment-1853177308) 显示 AirSim 录制图片中存在很多原图不存在的黑斑和阴影，明显是光影存在问题。
   - 目前在 UE5 archvis 项目以及其他一些项目中也存在不一致的情况，目前尚无明确解决方案，只能尝试多种引擎和版本的组合。
   - 2024/12/15 目前我的理解是，当前Colosseum 使用的方法是[GitHub](https://github.com/CodexLabsLLC/Colosseum/blob/main/Unreal/Plugins/AirSim/Source/UnrealImageCapture.cpp#L61C7-L61C7)先使用 `UTextureRenderTarget2D`和`USceneCaptureComponent2D`抓取图像之后使用 `render target` 进行渲染，然后我猜测 Colosseum 使用了UE4的渲染方式，导致`UE4` 和 `UE5` 最大的区别 `global lumin` 无法被渲染，目前猜测的解决办法是找到，UE5是如何抓取截图的 目前UE5的官方文档中无法搜索到 `render target` 我的理解是已经被更新了不过代码为了 backwards compatibility 依然能跑
   - 这功能理论上是非常常用的，只不过我目前仍无法看懂render的代码

4. **多种 segmentation 无法使用 AirSim 区分**
   - 首先需要将 foliage 里的 mesh 拆分出来，可参考[解决办法](https://dev.epicgames.com/community/snippets/zboW/unreal-engine-convert-foliage-instances-to-static-mesh-actors)。
   - 在编辑器中跑 AirSim 能抓到几百个物体，在编译后只剩下几十个，怀疑是被优化掉了，解决方法是在编辑器中直接操作。

## 记录表格
|         | Colosseum | czero    |
|---------|-----------|----------|
| UE 5.0  |   未测试   |          |
| UE 5.1  |   未测试       |          |
| UE 5.2  |    有光影瑕疵       |          |
| UE 5.3  |   不支持        |          |
