# CS4188/CS5188 VR 期末：GPT-5.5 模块化复习项目 Prompt 包

> 适用场景：你几乎 0 基础、只剩两天、资料很多、目标是通过 GPT-5.5 快速建立可考试输出的知识体系。  
> 核心原则：不要逐页读 PPT；按“模块 -> 输出 -> 检测 -> 纠错 -> 连接长题”的节奏复习。  
> 课程材料：Module Overview、1-9 讲 PPT、Tutorial 1-5、老师录音 transcript。  
> 考试情报：闭卷；无计算题；约 10 道 short questions、约 10 道 two-level multiple-choice、1 道 long question；三大主轴是 input/output devices、architecture、applications，而且会组合考。

---

## 0. 这个复习项目怎么用

每个模块都用同一个流程：

```text
1. 复制“项目总 instruction prompt”给 GPT-5.5，建立总规则。
2. 复制当前模块的“学习 prompt”。
3. 让 GPT-5.5 先讲概念，再出题测你。
4. 你闭卷作答。
5. 把你的答案发回 GPT-5.5，让它按考试标准批改。
6. 让 GPT-5.5 生成该模块“一页纸”。
7. 进入下一个模块。
```

每个模块的完成标准不是“看完了”，而是你能闭卷做到：

```text
定义说得出
机制讲得清
优缺点能比较
能举应用例子
能把它和 architecture / application / presence 连起来
```

---

# 1. 项目总 Instruction Prompt

下面这一段是你每次新开对话或重启复习时都可以复制给 GPT-5.5 的总指令。

```prompt
你是我的 CS4188/CS5188 Virtual Reality Technologies and Applications 期末复习教练。我的情况：这门课几乎没有上过，0 基础开始复习，只剩两天。我已经上传了课程所有 PPT、tutorial 和老师录音 transcript。请你严格基于这些材料帮我复习，不要泛泛讲 VR 常识。

考试情报如下：
- 闭卷。
- 不需要计算器。
- 老师说不会有计算题。
- 试卷大约包括：10 道 short questions，约 50 分；10 道 two-level multiple-choice questions，约 25 分；1 道 long question，约 25 分。
- 老师强调三大主题：input-output devices、architecture、applications。
- Architecture 中包括 pipeline architecture 和 distributed virtual environment。
- 题目可能会组合考，例如先问 architecture，再问 application。

你的教学目标：
1. 把我从 0 基础带到能应付期末考试。
2. 不要让我陷入 PPT 细节海；优先教高频、可答题、可组合的知识。
3. 每个知识点都按“定义 -> 直觉解释 -> 机制 -> 优缺点/trade-off -> 可能怎么考 -> 标准答案句子”讲。
4. 对公式只讲意义和变量关系；除非我要求，不做复杂推导，因为老师说无计算题。
5. 每个模块最后都必须给我：
   - 一页纸总结
   - 10 个核心术语
   - 5 道 short questions
   - 5 道 two-level multiple-choice questions
   - 1 道可能的 long-question 小片段
   - 我的闭卷自测任务
6. 当我回答题目后，你要按考试标准批改：指出漏点、错点、可加分表达，并给我可背诵的改进版答案。
7. 用中文讲解为主，关键术语保留英文。
8. 我时间紧，请你直接给结论和复习动作，不要废话。

每次开始一个模块时，请先输出：
- 本模块考试权重判断：高 / 中 / 低
- 本模块和三大考试主轴的关系
- 本模块最容易考的题型
- 本模块我必须掌握的 5-10 个核心问题
然后再开始教学。
```

---

# 2. 总复习模块地图

建议拆成 11 个模块。你不用平均用力，按优先级推进。

| 模块 | 名称 | 对应材料 | 优先级 | 建议时间 | 产出 |
|---|---|---|---|---:|---|
| M0 | 考试地图与 VR 总框架 | 录音 + Module Overview + Introduction | 最高 | 45 min | 总图 + 答题框架 |
| M1 | VR 基本概念与历史 | Introduction | 中 | 60 min | 定义、四层 VR、HCI |
| M2 | Input Devices 与 Tracking | Input Devices + Tutorial 1/2/3 | 最高 | 3 h | tracking 对比表 |
| M3 | Graphical Displays 与视觉系统 | Output Devices: Graphical Displays + Tutorial 4 | 最高 | 2 h | depth cues + HMD 问题 |
| M4 | Sound and Haptics | Output Devices: Sound and Haptics | 高 | 1.5 h | 3D sound + haptic 对比 |
| M5 | VR Modeling 与 Rendering Concepts | VR Modeling | 高 | 2 h | modeling 五类 + LoD/time-critical |
| M6 | Computing Architecture 与 Pipelines | Computing Architectures | 最高 | 2.5 h | graphics/haptics pipeline |
| M7 | Sense of Presence | Sense of Presence | 高 | 1 h | presence 增减因素 + 测量 |
| M8 | Distributed Virtual Environments | Distributed Virtual Environments | 最高 | 2 h | DVE/CVE + partitioning + latency |
| M9 | VR Applications | VR Applications | 最高 | 2 h | 应用模板 + 医疗案例 |
| M10 | Tutorials 原理复盘 | Tutorial 1-5 | 中 | 1.5 h | 只背原理，不推复杂公式 |
| M11 | 考前输出训练 | 全部材料 | 最高 | 3 h | short/MCQ/long question 套路 |

两天时间非常紧，真实优先级是：

```text
M0 -> M2 -> M3 -> M6 -> M8 -> M9 -> M7 -> M4 -> M5 -> M10 -> M11
```

---

# 3. M0：考试地图与 VR 总框架

## 本模块目标

先把这门课压缩成考试地图，避免你一上来被 700+ 页 PPT 拖死。

## 核心知识点

- 考试三大主轴：input-output devices、architecture、applications。
- Architecture 包括 pipeline architecture 与 distributed virtual environment。
- 题型：short questions、two-level multiple choice、long question。
- 答题基本结构：definition -> mechanism -> pros/cons -> application -> limitation/trade-off。
- 长题一定会需要把“设备 + 架构 + 应用 + presence”串起来。

## 学习 Prompt

```prompt
现在开始 M0：考试地图与 VR 总框架。

请你基于老师录音 transcript 和课程材料，帮我从 0 基础建立这门 VR 课的考试地图。请输出：

1. 老师录音透露的考试结构和复习策略。
2. 这门课所有 PPT 如何归入三大主题：input-output devices、architecture、applications。
3. 每个主题下面有哪些章节和核心问题。
4. 为什么不要逐页复习 PPT，而要按“定义-机制-比较-应用-trade-off”复习。
5. 给我一张 ASCII 总图，展示 VR 系统从 user input 到 virtual world update 到 output feedback 的流程。
6. 给我一套通用 short question 答题模板。
7. 给我一套 long question 答题模板：如果题目让我设计一个 VR training system，我应该从哪些角度答。
8. 最后用 5 道题测我是否理解考试地图。

请讲得适合 0 基础，但不要过度科普。我要能马上进入下一模块。
```

## 完成标准

你能闭卷写出：

```text
Input/Output Devices: how user communicates with VR system
Architecture: how the system updates and renders in real time
Applications: why and how VR is used in real-world domains
```

---

# 4. M1：VR 基本概念与历史

## 对应材料

- `1 - Introduction.pdf`
- `Module Overview.pdf`

## 核心知识点

### 4.1 VR Definition

VR 是一种 human-computer interface，包含：

```text
real-time simulation + interaction + multiple sensorial channels
```

可感官通道包括：visual、auditory、tactile、smell、taste。

### 4.2 Four levels of VR

| Level | 含义 | 例子 |
|---|---|---|
| Passive | 用户几乎不能控制 | 看电影、读书 |
| Exploratory | 能探索但不能修改 | 在虚拟世界中移动 |
| Interactive | 能探索也能操作对象 | 抓取虚拟物体 |
| Collaborative | 多用户共同交互 | 多人协作训练/游戏 |

### 4.3 HCI in VR

- Input：capture interaction instructions from user。
- Output：generate reactions back to user。
- VR 比传统 HCI 更强调 multi-sensory、real-time、interactive。

### 4.4 历史案例只记代表意义

- Sensorama：多感官沉浸机器，3D video、stereo sound、smell、wind、vibration。
- Sutherland HMD / Ultimate Display：早期 CG-based HMD。
- Flight simulator：军事训练驱动 VR。
- Oculus / modern VR：硬件、显示、传感器、game engine 成熟后复兴。

## 学习 Prompt

```prompt
现在开始 M1：VR 基本概念与历史。

我 0 基础，请你基于 Introduction PPT 帮我掌握考试会考的基础概念。请按下面结构讲：

1. VR 的标准定义：real-time simulation、interaction、multiple sensorial channels 分别是什么意思。
2. 为什么 VR 是一种 human-computer interface，而不只是 3D graphics。
3. passive / exploratory / interactive / collaborative 四层 VR 的区别，用生活例子解释。
4. input devices 和 output devices 在 VR 系统里分别负责什么。
5. VR 历史中只需要记哪些代表案例，以及它们各自说明了什么技术趋势。
6. 给我整理一张“术语 -> 中文解释 -> 考试答法”的表。
7. 出 5 道 short questions 和 5 道 two-level MCQ 测我。
8. 最后生成 M1 一页纸总结。

要求：不要展开太多历史细节，重点是能答题。
```

## 典型考法

- Define virtual reality。
- Compare four levels of VR。
- Explain why VR needs input and output devices。
- Explain why smell is less common in VR applications。

---

# 5. M2：Input Devices 与 Tracking

## 对应材料

- `2 - Input Devices.pdf`
- `Tutorial 1.pdf` Ultrasonic tracker
- `Tutorial 2.pdf` DC magnetic tracking
- `Tutorial 3.pdf` Locating markers with cameras
- `Tutorial 5.pdf` Marker-based AR 相关部分

## 优先级

最高。Input devices 是老师点名的三大考试主轴之一，而且非常适合 short questions 和 two-level MCQ。

## 核心知识点

### 5.1 Tracker

Tracker 是实时测量 position and/or orientation 的设备。VR 常追踪 head、hands、limbs。通常相对于 reference/world coordinate system 表示。

### 5.2 DOF

- 2 DOF：2D mouse。
- 3 DOF：只测 position 或 orientation 的某些维度。
- 6 DOF：position + orientation。

### 5.3 坐标变换链

```text
v2D = Mproj * Mview * Mworld * v3D
```

- Mworld：local/model -> world。
- Mview：world -> viewer/camera。
- Mproj：view -> 2D image。

### 5.4 Tracking performance 四指标

| 指标 | 记忆句 | 常见陷阱 |
|---|---|---|
| Accuracy | actual position 和 measured position 多接近 | 空间误差 |
| Jitter | 物体不动，输出还抖 | 随机波动 |
| Drift | 时间越久误差越大 | 时间累积 |
| Latency | 动作到反馈的延迟 | 会导致 sickness |

### 5.5 Tracker types 对比

| Type | Mechanism | Advantages | Drawbacks |
|---|---|---|---|
| Mechanical | links + joints | accurate, low latency | intrusive, heavy, limited motion |
| Magnetic | magnetic field transmitter/receiver | no line-of-sight | metal interference, limited range |
| Ultrasonic | time-of-flight | cheap/simple | low update rate, echo, line-of-sight |
| Optical | cameras + markers/features | precise, common in mocap | occlusion, calibration, ambiguity |
| Inertial | gyro/accelerometer/magnetometer | small, fast, cheap | drift/noise, needs fusion/reset |

### 5.6 Tutorial 只需掌握的原理

- Tutorial 1：ultrasonic tracker 通过 sound time-of-flight 求距离，再定位 microphone，两个 microphone 可求 orientation。
- Tutorial 2：magnetic field strength 与距离有关，可用不同 wire 的 magnetic reading 反推位置；方向用 right-hand rule。
- Tutorial 3：camera projection；多个 camera/known markers 可定位；共线会导致无唯一解。
- Tutorial 5：marker-based AR 用 marker 建立物理世界坐标系，并通过 camera calibration 获得 intrinsic parameters。

## 学习 Prompt

```prompt
现在开始 M2：Input Devices 与 Tracking。

我完全 0 基础，请你基于 Input Devices PPT 和 Tutorial 1/2/3/5，帮我掌握考试所需内容。请按以下结构输出：

1. 什么是 tracker，为什么 VR 需要 tracking。
2. DOF 是什么，2DOF/3DOF/6DOF 分别代表什么。
3. 用非常通俗的方式解释 v2D = Mproj * Mview * Mworld * v3D，每个矩阵在干什么。
4. 重点讲 accuracy、jitter、drift、latency 的区别。请给我一个“最容易混淆点”表。
5. 对比 mechanical / magnetic / ultrasonic / optical / inertial trackers：原理、优点、缺点、应用场景、考试关键词。
6. AC magnetic tracker 和 DC magnetic tracker 的区别，尤其 metal interference / eddy current / ferromagnetic metals。
7. optical tracking 中 outside-looking-in 和 inside-looking-out 的区别。
8. IMU 中 gyroscope、accelerometer、magnetometer 各自贡献什么，各自有什么问题。
9. Tutorial 1/2/3/5 不做复杂计算，只解释考概念时应如何回答。
10. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ、1 个 long-question 应用小题。
11. 最后生成 M2 一页纸总结。

请所有解释都服务考试，不要展开工程实现细节。
```

## 闭卷自测

你必须能不看资料回答：

```text
Explain accuracy, jitter, drift and latency.
Compare magnetic and optical trackers.
Why can magnetic trackers be affected by metal?
Why does latency cause simulation sickness?
How does ultrasonic tracking estimate position?
```

---

# 6. M3：Graphical Displays 与视觉系统

## 对应材料

- `3 - Output Devices (Graphical Displays).pdf`
- `Tutorial 4.pdf` Parallax barrier

## 优先级

最高。Output devices 是三大主轴之一，视觉显示又是 VR 最核心输出通道。

## 核心知识点

### 6.1 Human Visual System

- Retina：photoreceptors 分布不均。
- Fovea：中央区域，高分辨率、颜色感知。
- Peripheral vision：低分辨率但对 motion 敏感。
- Rods：night vision。
- Cones：color vision，L/M/S cones 对 red/green/blue 敏感。

### 6.2 FOV

- Each eye：约 150° horizontal，135° vertical。
- Both eyes combined：约 180° horizontal。
- Binocular overlap：约 120° horizontal。
- 大 FOV 提升 immersion/presence，但增加显示与渲染成本。

### 6.3 Depth cues

| Near object cues | Far object cues |
|---|---|
| convergence | occlusion |
| accommodation | perspective |
| disparity | haze |
| parallax | surface texture |

### 6.4 HMD image formation

- HMD 中 micro-display 很小。
- Lens magnifies image into larger, further virtual image。
- 好处：扩大视野、让眼睛更容易聚焦。

### 6.5 Convergence-accommodation conflict

HMD 高频考点：

```text
Eyes converge to virtual object depth, but accommodate to the fixed display/virtual image plane.
This mismatch causes discomfort and visual fatigue.
```

### 6.6 Display types

| Type | 重点 |
|---|---|
| HMD | 最沉浸，但有重量、FOV、分辨率、vergence-accommodation conflict |
| Hand-held display | 可进出 simulation，沉浸感较弱 |
| Autostereoscopic display | 不戴眼镜，但 viewing zone/resolution 问题 |
| Large-volume display | 支持多人/协作，但昂贵、同步复杂 |
| Volumetric display | 真实体显示，可 360° 看，但硬件复杂、分辨率限制 |

### 6.7 Tutorial 4: Parallax barrier

- 目标：left eye sees left image，right eye sees right image。
- Parallax barrier 通过 aperture 阻挡部分像素光线。
- 有 optimum viewing distance/location。
- 偏离最佳位置会出现 inverse image、blurred/blended zones。

## 学习 Prompt

```prompt
现在开始 M3：Graphical Displays 与视觉系统。

请基于 Output Devices (Graphical Displays) PPT 和 Tutorial 4，从 0 基础教我。请按以下结构讲：

1. 人眼视觉系统：retina、fovea、rods、cones、peripheral vision，各自为什么和 VR display 有关。
2. FOV 的几个关键数字，以及为什么 large FOV 会提高 presence 但增加技术成本。
3. depth perception：near cues 和 far cues 分别有哪些。请重点区分 convergence、accommodation、disparity、parallax。
4. HMD 如何用 lens 把小屏幕变成大而远的 virtual image。
5. 用非常通俗的方式解释 convergence-accommodation conflict，并给出考试标准答案。
6. 比较 HMD、hand-held display、autostereoscopic display、large-volume display、volumetric display。
7. 解释 parallax barrier 的原理、optimum viewing position、inverse image、blended zones。
8. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ、1 个 long-question 应用小题。
9. 最后生成 M3 一页纸总结。

请注意：我不需要复杂光学推导，只需要能应付闭卷概念题和比较题。
```

---

# 7. M4：Sound and Haptics

## 对应材料

- `4 - Output Devices (Sound and Haptics).pdf`

## 核心知识点

### 7.1 Sound properties

- Sound is a pressure wave propagating through a medium。
- Air speed about 343 m/s。
- Sound 有 reflection、refraction、diffraction。

### 7.2 Human auditory system

- Pinna 会改变频率响应，帮助判断方向。
- Ear canal 放大 3-12 kHz。
- 人耳范围约 20 Hz-20 kHz。
- 人对 3-4 kHz 最敏感。

### 7.3 3D sound

3D sound 与 stereo sound 的区别：

```text
3D sound changes according to the location and orientation of the user's head.
```

### 7.4 Sound localization cues

| Cue | 用途 | 关键词 |
|---|---|---|
| ITD | horizontal/azimuth | time difference between ears |
| IID | horizontal/azimuth | intensity difference, head-shadow effect |
| Pinna filtering | elevation | outer ear changes frequencies |
| Loudness/prior knowledge | distance | whisper vs siren |
| Motion parallax | distance/orientation | head movement changes perceived direction |

### 7.5 HRTF

- HRTF = Head-Related Transfer Function。
- 描述 sound source 到 ear 的频率响应变化。
- 个体差异大；错误 HRTF 可能导致 front-back confusion。

### 7.6 Haptics

| Type | 感觉 | 例子 |
|---|---|---|
| Tactile feedback | touch sensation | vibration, texture, pressure, temperature |
| Force feedback | force/torque | weight, resistance, collision, inertia |

### 7.7 Haptic system 注意点

- Force feedback 更难，因为要稳定、安全、低延迟。
- Haptics 对 medical training / surgery simulation 很重要。
- Haptic rendering 往往需要比 graphics 更高更新率。

## 学习 Prompt

```prompt
现在开始 M4：Sound and Haptics。

请基于 Output Devices (Sound and Haptics) PPT，从 0 基础帮我复习。请按以下结构输出：

1. sound 的基本物理属性：pressure wave、speed、reflection/refraction/diffraction。
2. 人耳如何帮助定位声音：pinna、ear canal、frequency sensitivity。
3. stereo sound 和 3D sound 的区别。
4. sound localization：ITD、IID、elevation cues、distance cues、motion parallax。每个都要用一句考试可背答案解释。
5. HRTF 是什么，为什么它和 3D sound/presence 有关。
6. tactile feedback 和 force feedback 的区别。
7. 为什么 haptics 对 medical/surgical VR 特别重要。
8. haptic feedback 的技术难点：latency、stability、safety、intrusiveness。
9. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ、1 个 long-question 应用小题。
10. 最后生成 M4 一页纸总结。

请不要做复杂公式，重点是概念、比较、应用。
```

---

# 8. M5：VR Modeling 与 Rendering Concepts

## 对应材料

- `6 - VR Modeling.pdf`
- 部分 `5 - Computing Architectures for VR.pdf`

## 优先级

高。它常常不会单独作为最大题，但会在 long question 中作为“虚拟世界怎么建模/怎么优化”的加分点。

## 核心知识点

### 8.1 VR object modeling issues

五类建模问题：

```text
1. Geometric modeling
2. Kinematical modeling
3. Physical modeling / interactions
4. Object behavior modeling / intelligent agents
5. Model management
```

### 8.2 Geometric modeling

- Polygonal meshes：最常用，尤其 triangular mesh，因为 computationally efficient。
- Splines/NURBS：曲面更平滑，存储效率可能更好。
- Point cloud：scanner 输出，经转换可变 mesh/surface。

### 8.3 Object appearances

- Local illumination：flat / Gouraud / Phong shading。
- Global illumination：考虑 inter-reflection 和 shadows，更真实但更贵。
- Texture mapping：像贴纸，可以提升 realism、spatial cues，并减少 polygon 数量。

### 8.4 Kinematical modeling

描述 object 如何运动：

- open-chain structures
- closed-chain structures
- inverse kinematics
- motion constraints

### 8.5 Physical modeling

- Collision detection。
- Collision response。
- Deformable objects。
- Particle systems / fluids / cloth 等可作为案例。

### 8.6 Model management

- Level of Detail (LoD)：远处/不重要物体用低细节模型，提高 frame rate。
- Time-critical rendering：在固定 frame deadline 内最大化图像质量。
- Visibility culling / occlusion culling：不渲染看不见的东西。

## 学习 Prompt

```prompt
现在开始 M5：VR Modeling 与 Rendering Concepts。

请基于 VR Modeling PPT，从 0 基础帮我复习。请按以下结构输出：

1. VR modeling 在整个 VR system architecture 中的位置：它为 VR engine 提供什么。
2. 五类 object modeling issues：geometric、kinematical、physical、behavior、model management。每类用一句话解释和一个例子。
3. geometric modeling：polygonal meshes、triangular meshes、splines、point cloud、scanner data，各自适合什么。
4. object appearance：local illumination、global illumination、texture mapping。重点讲它们对 realism 和 frame rate 的影响。
5. flat / Gouraud / Phong shading 的区别，按考试比较题讲。
6. physical modeling：collision detection/response、deformation、particle/fluid/cloth，只讲概念和考点。
7. model management：LoD、culling、time-critical rendering。重点讲为什么 VR 需要它们。
8. 把本模块和 architecture / applications 连接起来：例如医疗训练、制造仿真、游戏为什么需要不同建模。
9. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ、1 个 long-question 应用小题。
10. 最后生成 M5 一页纸总结。

请不要陷入数学和渲染算法细节，重点是考试答题。
```

---

# 9. M6：Computing Architecture 与 Pipelines

## 对应材料

- `5 - Computing Architectures for VR.pdf`

## 优先级

最高。Architecture 是老师点名三大主轴之一，并且容易和 application 组合成长题。

## 核心知识点

### 9.1 VR system architecture tasks

每一轮 VR 系统做：

```text
1. read input devices
2. update state of virtual world
3. render outputs: graphics/haptics/audio
4. feed outputs to output devices
```

### 9.2 VR engine needs

- Low latency。
- Fast graphics rendering。
- Haptics rendering。

### 9.3 Graphics rendering pipeline

三阶段：

| Stage | Runs on | Tasks |
|---|---|---|
| Application stage | CPU | read input, update world, select objects |
| Geometry stage | GPU | transformations, shading, projection, clipping |
| Rasterizer stage | GPU | fragments/pixels, anti-aliasing, texture mapping |

### 9.4 Phong illumination / shading

不需要背完整公式，重点是三部分：

```text
ambient + diffuse + specular
```

Shading models：

| Model | Meaning | Quality/Cost |
|---|---|---|
| Flat | one color per polygon | cheap, faceted |
| Gouraud | interpolate vertex colors | medium |
| Phong | interpolate normals, compute per-pixel light | realistic, expensive |

### 9.5 Anti-aliasing

- 问题：aliasing/jagged edges。
- 原理：sub-samples per pixel，再 average color。
- trade-off：more sub-samples -> better quality but higher cost。

### 9.6 Haptics rendering pipeline

通常包括：

```text
collision detection -> collision response -> force computation -> force output
```

Haptics 比 graphics 对 latency 更敏感，更新率通常更高。

### 9.7 Bottleneck 判断

| 现象 | 可能瓶颈 | 优化方向 |
|---|---|---|
| CPU full | application stage | reduce simulation/update logic |
| many lights/polygons slow | geometry stage | reduce geometry/lights/shading cost |
| high resolution slow | rasterizer stage | reduce resolution/samples/textures |
| haptic unstable | haptics loop | reduce delay / simplify collision |

## 学习 Prompt

```prompt
现在开始 M6：Computing Architecture 与 Pipelines。

请基于 Computing Architectures for VR PPT，从 0 基础帮我复习。请按以下结构讲：

1. VR system 每一帧/每一循环要完成哪些任务：input -> update world -> render output -> output devices。
2. 为什么 VR engine 需要 low latency、fast graphics rendering、haptics rendering。
3. graphics rendering pipeline 三阶段：application stage、geometry stage、rasterizer stage。每阶段在哪里运行、做什么、可能出现什么 bottleneck。
4. illumination 和 shading：ambient/diffuse/specular，flat/Gouraud/Phong shading。不要讲复杂公式，讲考试答法。
5. anti-aliasing：为什么会有 aliasing，subsampling 如何解决，代价是什么。
6. texture mapping 在 rasterizer stage 的作用，以及它为什么能增加 realism 和减少 polygons。
7. haptics rendering pipeline：collision detection、collision response、force computation、force output。
8. graphics pipeline 和 haptics pipeline 的区别，尤其更新率和 latency 要求。
9. 如何把 architecture 用到 long question：比如设计 medical training VR system 时该怎么写架构。
10. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ、1 个 long-question 应用小题。
11. 最后生成 M6 一页纸总结。

请把这个模块讲成“考试长题可直接套用”的架构模板。
```

---

# 10. M7：Sense of Presence

## 对应材料

- `7 - Sense of Presence.pdf`

## 优先级

高。Presence 是非常适合连到设备、延迟、应用设计的概念，长题很好用。

## 核心知识点

### 10.1 Definition

Sense of presence：

```text
the feeling of being there in a virtual environment
```

### 10.2 为什么难实现

因为要让视觉、听觉、触觉、运动、嗅觉等感官都相信自己真的在环境里。

### 10.3 Sheridan 三个 physical variables / metrics

```text
1. extent of sensory information
2. control of sensors
3. ability to modify the environment
```

### 10.4 Measuring presence

| Measure | 含义 | 例子 |
|---|---|---|
| Subjective | questionnaires | “how real did it feel?” Likert scale |
| Psychophysical | relate stimulus magnitude to rating | resolution/latency/FOV vs rating |
| Objective | physiological/performance | heart rate, blood pressure, task time |

### 10.5 What increases presence

- High visual quality。
- Large FOV。
- Low latency。
- Head tracking。
- Multiple senses。
- Interactivity。
- Seeing user's own body parts。

### 10.6 What decreases presence

- Disjoint senses / sensory mismatch。
- High latency。
- Poor interactivity。
- Cables。
- Low quality audio。
- Cannot see user's own body parts。

## 学习 Prompt

```prompt
现在开始 M7：Sense of Presence。

请基于 Sense of Presence PPT，从 0 基础帮我复习。请按以下结构输出：

1. sense of presence 的定义，用中文解释“being there”。
2. 为什么 presence 难实现：多感官一致性、现实感、交互性。
3. Sheridan 的三个 physical variables/metrics：extent of sensory information、control of sensors、ability to modify environment。每个给例子。
4. presence 的三类测量：subjective、psychophysical、objective。每类举例。
5. 什么因素增加 presence：visual quality、FOV、latency、head tracking、multiple senses、interactivity、body visibility。
6. 什么因素降低 presence：sensory mismatch、high latency、poor interactivity、cables、low audio quality、no body visibility。
7. 把 presence 和前面模块连接起来：HMD、3D sound、haptics、tracking、DVE latency、medical training。
8. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ、1 个 long-question 应用小题。
9. 最后生成 M7 一页纸总结。

请重点帮我形成长题表达：如何设计一个 high-presence VR system。
```

---

# 11. M8：Distributed Virtual Environments

## 对应材料

- `9 - Distributed Virtual Environments.pdf`
- `5 - Computing Architectures for VR.pdf` 中 Distributed VR Architecture 相关部分

## 优先级

最高。老师录音明确把 distributed virtual environment 放进 architecture 主题中。

## 核心知识点

### 11.1 DVE / CVE

- DVE：shared virtual environment，remote users interact with virtual objects/tasks through networks。
- CVE：DVE 中支持 multiple users perform a task together。

### 11.2 为什么 DVE 难

- 强调 interactivity。
- 用户期望 instant response。
- 单服务器要处理 all clients、update avatars/objects、distribute messages。
- 用户增多后 server overloaded。

### 11.3 Multi-server architectures

| Method | Principle | Advantage | Drawback |
|---|---|---|---|
| User partitioning | users assigned to different servers | simple | different servers cannot interact |
| Region partitioning | VE divided into fixed regions | spatial load division | fixed regions can overload if popularity shifts |
| Dynamic partitioning | regions adjusted at runtime | adaptive | complex, needs regular/local repartitioning |

### 11.4 Network latency

- LAN latency 小，overseas latency 大。
- Discrete events：time gaps larger than network delay，影响较小。
- Continuous events：time gaps smaller than network delay，影响很大，例如 3D game interactions。

### 11.5 Motion synchronization

典型问题：两个用户几乎同时操作同一对象，各自本地状态不一致。

常见处理：

```text
winner decision + rollback/correction
```

Rollback：把 illegal/wrong state 强制修正到 correct state。

### 11.6 DVE 与 long question

DVE 可连接：

- online games。
- virtual museum。
- metaverse。
- collaborative medical/military training。
- remote education。

## 学习 Prompt

```prompt
现在开始 M8：Distributed Virtual Environments。

请基于 Distributed Virtual Environments PPT 和 Computing Architectures 中相关内容，从 0 基础帮我复习。请按以下结构输出：

1. DVE 和 CVE 的定义与区别。
2. 为什么 DVE 特别强调 interactivity 和 instant response。
3. 单服务器 client-server 架构为什么会 overloaded。
4. 对比 user partitioning、region partitioning、dynamic partitioning：原理、优点、缺点、适用场景、考试关键词。
5. network latency 为什么对 DVE 特别严重。
6. discrete events 和 continuous events 的区别，分别受 latency 影响如何。
7. 用通俗例子解释两个用户同时移动同一个 object 时会发生什么 synchronization problem。
8. rollback/correction 是什么，为什么会影响 user experience。
9. 把 DVE 和 applications 连接：online game、virtual museum、collaborative training、metaverse。
10. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ、1 个 long-question 应用小题。
11. 最后生成 M8 一页纸总结。

请把本模块讲成 architecture 高频考点，尤其注意比较题和长题。
```

---

# 12. M9：VR Applications

## 对应材料

- `8 - VR Applications.pdf`
- `7 - Sense of Presence.pdf`
- 其他设备与架构章节作为支撑

## 优先级

最高。Applications 是老师点名三大主题之一，也是 long question 的天然载体。

## 核心知识点

### 12.1 Application categories

```text
1. Medical applications
2. Entertainment / arts / education
3. Defense / aerospace
4. Manufacturing
5. Robotics
6. Emerging applications
```

### 12.2 Medical applications 为什么重要

VR 适合医疗训练，因为：

- train medical students and doctors。
- allow errors on virtual patients, not real ones。
- model rare cases。
- reduce cadaver shortage / animal rights issue。
- reduce cost。
- support repeated practice and assessment。

### 12.3 Medical examples

| Example | 考试关键词 |
|---|---|
| EMR to bio-terrorism | stressful situation awareness, virtual casualties, timing matters |
| Virtual anatomy | cadaver scarce, repeated exploration, interactive 3D model |
| DRE trainer | haptics/PHANToM, diagnosis training |
| Endoscopy / colonoscopy | invasive procedure training, risk reduction, 3D reconstruction |
| MIS | hand motion vs tool tip motion, limited vision, practice |
| Rehabilitation | repetition, monitoring, motivation, remote feedback |

### 12.4 Defense / aerospace

- Dangerous/expensive training can be simulated。
- Flight simulators are classic VR applications。
- Allows repeated training without real-world risk。

### 12.5 Manufacturing

- Virtual prototyping。
- Assembly/disassembly planning。
- Ergonomic analysis。
- Training workers safely。

### 12.6 Robotics / Telepresence

- Remote operation。
- Visual/haptic feedback。
- Useful when environment is dangerous or inaccessible。

### 12.7 Long question 通用模板

如果题目让你设计一个 VR application，按这个答：

```text
1. Application goal and users
2. Input devices: tracking, gesture, controllers, sensors
3. Output devices: HMD/display, 3D sound, haptics
4. Modeling: geometry, physical interactions, behavior/state machines
5. Architecture: input loop, world update, graphics/haptics rendering pipeline
6. Presence: FOV, low latency, interactivity, multisensory feedback
7. Distributed issues if multi-user: DVE/CVE, synchronization, partitioning
8. Benefits: safety, cost, repeatability, rare cases
9. Limitations: latency, accuracy, cost, sickness, training transfer
```

## 学习 Prompt

```prompt
现在开始 M9：VR Applications。

请基于 VR Applications PPT，从 0 基础帮我复习。请按以下结构输出：

1. VR applications 的六大类别。
2. 为什么 medical applications 是重点：从 safety、cost、rare cases、repeatability、assessment 角度解释。
3. 逐个解释核心医疗案例：EMR bio-terrorism、virtual anatomy、DRE trainer、endoscopy/colonoscopy、MIS、rehabilitation。每个只抓考试关键词，不背细枝末节。
4. defense/aerospace、manufacturing、robotics/telepresence 各自为什么适合 VR。
5. 每个 application 如何连接 input devices、output devices、modeling、architecture、presence。
6. 给我一套 long question 通用答题模板：Design a VR system for X。
7. 给我 2 个完整长题范例答案：
   - Design a VR medical training system。
   - Design a collaborative VR training system。
8. 给我 10 个核心术语、5 道 short questions、5 道 two-level MCQ。
9. 最后生成 M9 一页纸总结。

请重点训练我把前面所有模块综合进 application，不要只讲案例故事。
```

---

# 13. M10：Tutorials 原理复盘

## 对应材料

- `Tutorial 1.pdf`
- `Tutorial 2.pdf`
- `Tutorial 3.pdf`
- `Tutorial 4.pdf`
- `Tutorial 5.pdf`

## 优先级

中。老师说无计算题，所以不要花太多时间推公式。但 tutorial 会帮助你理解设备原理，选择题可能考概念。

## Tutorial 1：Ultrasonic Tracker

必会原理：

- speaker 发 ultrasonic sound。
- microphone 接收声音。
- time-of-flight × speed of sound = distance。
- 两个 speaker 到一个 microphone 的距离可定位该 microphone。
- 两个 microphone 的位置可求 tracker orientation。

## Tutorial 2：DC Magnetic Tracking

必会原理：

- straight wire current creates magnetic field。
- magnetic field magnitude 与距离有关。
- magnetometer reading 可用于反推位置。
- magnetic field direction 用 right-hand rule 判断。

## Tutorial 3：Locating Markers with Cameras

必会原理：

- 3D point projects to image plane。
- image coordinate depends on camera position, focal length/FOV, object position。
- camera calibration 估计 camera parameters。
- 多个 camera observing same point 可 reconstruct 位置。
- 如果 known points 和 camera center 共线，可能没有唯一解。

## Tutorial 4：Parallax Barrier

必会原理：

- glasses-free 3D。
- left eye sees left image，right eye sees right image。
- barrier aperture blocks pixels selectively。
- 偏离 optimum viewing location 会 inverse/blend/blur。

## Tutorial 5：Marker-based AR

必会原理：

- AR pipeline：physical coordinate system -> anchor digital content -> track camera pose -> project content。
- marker 提供物理世界坐标系。
- ArUco marker：black border + binary matrix ID/error correction。
- camera calibration 获取 intrinsic parameters。
- marker detection 可得到 marker ID 和 camera pose relative to marker。

## 学习 Prompt

```prompt
现在开始 M10：Tutorials 原理复盘。

请基于 Tutorial 1-5，帮我用“无计算题”的方式复习 tutorial。要求：

1. 每个 tutorial 只讲考试可能考的概念原理，不推复杂公式。
2. 对 Tutorial 1：解释 ultrasonic tracker 如何通过 time-of-flight 定位和求 orientation。
3. 对 Tutorial 2：解释 DC magnetic tracking 如何由 magnetic field strength 反推位置，以及 right-hand rule 的意义。
4. 对 Tutorial 3：解释 camera projection、camera calibration、multi-camera localization，以及什么情况下没有 unique solution。
5. 对 Tutorial 4：解释 parallax barrier、autostereoscopic display、optimum viewing position、inverse image、blended zones。
6. 对 Tutorial 5：解释 marker-based AR pipeline、ArUco marker、camera intrinsic/extrinsic parameters。
7. 每个 tutorial 给我：核心原理、可能选择题陷阱、1 道 short question 标准答案。
8. 最后做一张 Tutorial 1-5 总表。

注意：老师说期末无计算题，所以请你压缩公式，只保留变量关系和直觉。
```

---

# 14. M11：考前输出训练

## 对应材料

- 全部材料
- 你前面每个模块的一页纸总结

## 优先级

最高。最终真正提分的是输出，不是继续看资料。

## 训练结构

### 14.1 Short Questions

练习目标：用 4-8 句话快速答概念。

标准结构：

```text
Definition.
Mechanism / explanation.
One advantage or issue.
Application/example if relevant.
```

### 14.2 Two-level MCQ

老师说选择题是 two-level。你的解题动作：

```text
1. 先判断第一层事实是否正确。
2. 再判断第二层理由是否正确。
3. 再判断理由是否真正解释第一层。
4. 不要因为关键词熟悉就选。
```

### 14.3 Long Question

长题通用结构：

```text
Paragraph 1: Define the target application and users.
Paragraph 2: Input devices and tracking.
Paragraph 3: Output devices: graphics, sound, haptics.
Paragraph 4: Modeling: geometry, physics, behavior, LoD.
Paragraph 5: Architecture: input loop, world update, graphics/haptics pipeline.
Paragraph 6: Presence and usability: low latency, FOV, multisensory, interactivity.
Paragraph 7: Distributed issues if multi-user.
Paragraph 8: Benefits and limitations.
```

## 学习 Prompt

```prompt
现在开始 M11：考前输出训练。

请你扮演 CS4188/CS5188 VR 期末出题老师和严厉阅卷老师。我已经学完所有模块，现在要做闭卷输出训练。请你按真实考试风格出题并批改。

第一轮请输出：
1. 10 道 short questions，覆盖 input/output devices、architecture、applications、presence、DVE、tutorial concepts。
2. 10 道 two-level multiple-choice questions。每道题都要有 Statement A 和 Reason B，让我判断 A/B 是否正确以及 B 是否解释 A。
3. 1 道 25 分 long question，要求我设计或分析一个 VR system，必须综合 input/output devices、architecture、applications。

出题后请先不要给答案。等我回答后，你再：
1. 按分点批改。
2. 标出我漏掉的关键词。
3. 给出可背诵的标准答案。
4. 总结我最薄弱的 3 个模块。
5. 给我最后 2 小时冲刺建议。
```

---

# 15. 两天执行计划：按模块跑 GPT-5.5

## Day 1

| 时间 | 模块 | 目标 |
|---|---|---|
| 09:00-09:45 | M0 | 建考试地图 |
| 09:45-10:45 | M1 | VR 定义与四层框架 |
| 10:45-13:00 | M2 上半 | tracking 指标 + tracker types |
| 14:00-15:30 | M2 下半 | optical / IMU / tutorial 1-3 原理 |
| 15:30-17:30 | M3 | graphical displays + HMD + depth cues |
| 19:00-20:00 | M4 | sound + haptics |

> 20:00 后不要扩展新内容。只整理当天一页纸，做 10 分钟闭卷复述，然后收工。

## Day 2

| 时间 | 模块 | 目标 |
|---|---|---|
| 09:00-10:30 | M6 | architecture + pipelines |
| 10:30-12:00 | M8 | DVE + latency + partitioning |
| 13:00-14:00 | M7 | presence |
| 14:00-15:30 | M5 | modeling + LoD/time-critical |
| 15:30-17:00 | M9 | applications + long question 模板 |
| 17:00-18:00 | M10 | tutorials 原理复盘 |
| 19:00-20:00 | M11 | 第一轮模拟题 |
| 20:00 后 | 只看错题 | 不学新内容 |

---

# 16. 每个模块都要让 GPT-5.5 生成的固定产物

每学完一个模块，复制这个 prompt：

```prompt
请把刚才这个模块压缩成“考前一页纸”。要求：

1. 只保留考试会用的内容。
2. 每个术语给一句英文关键词和一句中文解释。
3. 输出：
   - 10 个必背术语
   - 5 个高频比较
   - 5 个可能 short question 的标准答案句
   - 3 个 two-level MCQ 陷阱
   - 1 个如何连接 long question 的段落模板
4. 最后给我一个 3 分钟闭卷复述脚本。
```

---

# 17. 我的闭卷答题 Prompt

当你想自测时，用这个：

```prompt
请开始闭卷自测。你现在不要讲解，直接问我题。

范围：刚学完的模块。
题型：
1. 3 道定义题。
2. 3 道比较题。
3. 2 道机制解释题。
4. 2 道 application connection 题。

要求：
- 一次只问一题。
- 我回答后你立即批改。
- 批改时给分，满分 5 分。
- 指出我漏掉的关键词。
- 给我一版可背诵答案。
- 如果我连续两题低于 3 分，请暂停并重讲该知识点。
```

---

# 18. 最终长题万能 Prompt

在考试前最后 3 小时用：

```prompt
请用 CS4188/CS5188 VR 期末 long question 风格训练我。请你出 3 道可能的 25 分长题，每题都要求综合 input/output devices、architecture、applications。题目可以围绕：

1. VR medical training system
2. collaborative virtual environment / metaverse
3. VR manufacturing or aerospace training system

每道题请先只给题目和评分 rubrics，不要给答案。等我作答后，请按 25 分制批改，并给出高分答案结构。

批改重点：
- 是否定义应用目标
- 是否选择合适 input devices
- 是否选择合适 output devices
- 是否解释 architecture/pipeline
- 是否考虑 modeling
- 是否考虑 presence/latency/sickness
- 是否考虑 distributed synchronization if applicable
- 是否说明 benefits and limitations
```

---

# 19. 最后必须背熟的总表

## 19.1 三大主轴

```text
Input-output devices:
How the user senses and acts in the VR world.

Architecture:
How the system updates, renders, synchronizes and keeps latency low.

Applications:
Why VR is useful in real-world tasks and how to design a VR system for them.
```

## 19.2 最容易跨模块组合的概念

| 概念 | 可连接模块 |
|---|---|
| Latency | tracking, graphics, haptics, DVE, presence, sickness |
| FOV | graphical display, presence, HMD design |
| Haptics | output devices, medical applications, haptic pipeline |
| Tracking accuracy | input devices, interaction, medical/surgical precision |
| DVE synchronization | architecture, applications, online games, collaborative training |
| LoD/time-critical rendering | modeling, architecture, real-time VR |
| Presence | all output devices, interactivity, body visibility, applications |

## 19.3 长题开头万能句

```text
A VR system for this application should support real-time simulation, interactive user input, and multisensory feedback. Therefore, the design should consider input tracking devices, graphical/audio/haptic output devices, modeling of the virtual environment, low-latency rendering architecture, and factors that increase the user's sense of presence.
```

## 19.4 长题结尾万能句

```text
The main advantages of such a VR system are safety, repeatability, lower cost, and the ability to simulate rare or dangerous scenarios. However, its effectiveness depends on tracking accuracy, low latency, realistic visual/haptic feedback, and the extent to which training performance transfers to the real world.
```

---

# 20. 最后提醒

你现在不是要“学懂整个 VR 学科”，而是要在两天内把材料变成可答题输出。每个模块都必须以输出结束：

```text
一页纸
闭卷复述
短答题
选择题陷阱
长题连接
```

不要追求漂亮笔记。追求考场能写出来。
