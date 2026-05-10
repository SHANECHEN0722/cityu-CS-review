
# CS5182 Computer Graphics 模拟期中测试 (Mock Mid-term Quiz)
**注意：本试卷包含 10 道题目。请在答题区写下你的答案。**

### 题目 (Questions)
**1. 简述多边形网格（Polygon Meshes）作为 3D 对象表示方法的两个主要优点和两个主要缺点。**
**2. 在进行 2D 直线绘制时，Bresenham 画线算法（Bresenham's line algorithm）的核心思想和主要步骤是什么？（请列出 6 个基本步骤）**
**3. 在 3D 齐次坐标系下，请写出以下两种几何变换的 4×4 变换矩阵：**
(A) 绕 y 轴旋转 $\theta$ 角度。
(B) 沿向量 $v=(t_x, t_y, t_z)$ 进行平移。
**4. 在裁剪（Clipping）阶段，Cohen-Sutherland 线段裁剪算法使用了 4 位区域编码（4-bit code-words）。请写出该算法中判定线段被“平凡接受（Trivial accept）”和“平凡拒绝（Trivial reject）”的具体条件。**
**5. 请列举平行投影（Parallel projection）和透视投影（Perspective projection）之间的主要区别，并说明透视投影相对于平行投影的一个主要视觉优势。**
**6. Phong 光照模型（Phong Illumination Model）包含哪三个主要的光照分量？请分别写出它们的名称并简述其含义。**
**7. 深度缓冲算法（Z-buffering method）是目前最常用的隐藏面消除算法之一。请简述该算法的基本工作原理。**
**8. 请按先后顺序列出图形渲染管线（The Rendering Pipeline）中包含的主要阶段（Stages）。**
**9. 光栅化渲染（Rasterization rendering）与光线追踪（Ray tracing）是两种不同的渲染架构。请简述光线追踪算法的基本追踪方向，并列举它的一个主要优点和一个主要缺点。**
**10. 辐射度算法（Radiosity）主要用于解决光线追踪算法无法处理的哪种具体光照现象？它的计算结果是否依赖于观察者的视角（View-dependent/View-independent）？**

---

### 参考答案 (Answers)
**1. 简述多边形网格（Polygon Meshes）作为 3D 对象表示方法的两个主要优点和两个主要缺点。**

- **答案：**
  - 优点：(1) 非常灵活，可以表达复杂的细节；(2) 容易修改（如平滑、细分、变形等）；(3) 渲染处理效率高。
  - 缺点：(1) 受分辨率限制，高细节模型需要密集的网格，内存和计算开销大；(2) 因为是用平面近似曲面，会存在一定的视觉误差；(3) 拓扑结构复杂，难以处理非流形边（non-manifold edges）和洞。
**2. 在进行 2D 直线绘制时，Bresenham 画线算法（Bresenham's line algorithm）的核心思想和主要步骤是什么？（请列出 6 个基本步骤）**

- **答案：**
  1. 将 x 设为起点 $x_1$，y 设为 $y_1$，并为该像素着色。
  2. x 坐标增加 1，对应的 y 坐标更新为 $y = y + m$。
  3. 计算 D1：点 $(x, y)$ 距离上方像素中心的距离。
  4. 计算 D2：点 $(x, y)$ 距离下方像素中心的距离。
  5. 如果 $D1 < D2$（即线段更靠近上方像素），则绘制上方像素；否则，绘制下方像素。
  6. 如果未达到终点 $(x_2, y_2)$，则返回步骤 2)；否则，停止。
**3. 在 3D 齐次坐标系下，请写出以下两种几何变换的 4×4 变换矩阵。**

- **答案：**
(A) 绕 y 轴旋转 $\theta$ 角度矩阵：
$R_y = \begin{bmatrix} cos\theta & 0 & sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -sin\theta & 0 & cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$
(B) 沿向量平移矩阵：
$T = \begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}$
**4. 在裁剪（Clipping）阶段，Cohen-Sutherland 线段裁剪算法使用了 4 位区域编码（4-bit code-words）。请写出该算法中判定线段被“平凡接受（Trivial accept）”和“平凡拒绝（Trivial reject）”的具体条件。**

- **答案：**
  - **平凡接受：** 如果线段两个端点的编码皆为 "0000"（即两个端点编码的按位或（OR）操作结果为 0），说明线段完全在裁剪区域内部，直接接受。
  - **平凡拒绝：** 如果线段两个端点的编码在同一位上都为 1（即两个端点编码的按位与（AND）操作结果不为 0），说明线段完全在裁剪区域外部的同一侧，直接拒绝。
**5. 请列举平行投影（Parallel projection）和透视投影（Perspective projection）之间的主要区别，并说明透视投影相对于平行投影的一个主要视觉优势。**

- **答案：**
  - **区别：** 平行投影的投影中心（COP）在无限远，所有的投射线相互平行，并且保持对象的几何平行性不变；而透视投影的投影中心（COP）在有限距离，所有的投射线在 COP 处相交，通常无法保持几何体的平行性。
  - **透视投影的优势：** 透视投影能够提供深度感（Depth information/Foreshortening），产生近大远小的真实视觉效果。
**6. Phong 光照模型（Phong Illumination Model）包含哪三个主要的光照分量？请分别写出它们的名称并简述其含义。**

- **答案：**
  1. **环境光反射（Ambient reflection，Ia​）：** 一种统一的光照强度，独立于表面位置和观察视角，模拟光线在场景中多次散射后的基础照明。
  2. **漫反射（Diffuse reflection，Id​）：** 光线照射到粗糙表面后向各个方向均匀反射的现象，其强度取决于光线向量与表面法线之间的夹角。
  3. **镜面反射（Specular reflection，Is​）：** 处理光滑表面上的高光（Highlights）现象，其强度取决于视线向量与反射光线向量之间的夹角。
**7. 深度缓冲算法（Z-buffering method）是目前最常用的隐藏面消除算法之一。请简述该算法的基本工作原理。**

- **答案：**
Z-buffer 算法使用两个缓冲区：帧缓冲区（Frame buffer，用于存储像素颜色）和深度缓冲区（Depth buffer，用于存储像素当前的最小 Z 值/深度）。
在渲染过程中，算法会计算每一个即将被写入多边形的像素的深度。如果该像素的新深度值小于深度缓冲区中记录的当前深度值（意味着它离观察者更近），则更新帧缓冲区中的颜色，并将新的深度值写入深度缓冲区。否则，丢弃该像素。
**8. 请按先后顺序列出图形渲染管线（The Rendering Pipeline）中包含的主要阶段（Stages）。**

- **答案：**
(1) 输入对象模型（Input object models）
(2) 世界坐标变换（World coordinate transformation）
(3) 透视变换（Perspective transformation）
(4) 背面剔除（Back-face removal）
(5) 裁剪（Clipping）
(6) 光栅化（Rasterization）
(7) 隐藏面消除与着色（Hidden surface removal and shading）
*(最后输出图像 Output image)*
**9. 光栅化渲染（Rasterization rendering）与光线追踪（Ray tracing）是两种不同的渲染架构。请简述光线追踪算法的基本追踪方向，并列举它的一个主要优点和一个主要缺点。**

- **答案：**
  - **追踪方向：** 采取反向追踪（Backward manner），即从观察者（眼睛/相机）穿过图像平面上的像素向场景内发射光线，直到击中光源。
  - **优点：** 能够完美地计算直接和间接的镜面反射（reflections）、折射（refractions）以及清晰的阴影。
  - **缺点：** 计算效率低（耗时极大），并且无法计算物体间的间接漫反射（indirect diffuse reflections）。
**10. 辐射度算法（Radiosity）主要用于解决光线追踪算法无法处理的哪种具体光照现象？它的计算结果是否依赖于观察者的视角（View-dependent/View-independent）？**

- **答案：**
  - 辐射度算法主要用于精确计算整个场景内部表面之间的**间接漫反射（Indirect diffuse reflections / scattering between objects）**。
  - 它的计算结果是**与视角无关的（View-independent）**，因为漫反射的光能是在各个方向上均匀辐射的。

# CS5182 Computer Graphics Mock Mid-term Quiz
**Notice: This paper contains 10 questions. Please write your answers in the designated areas.**

### Questions
**1. Briefly describe two main advantages and two main disadvantages of Polygon Meshes as a representation of 3D objects.**
**2. What are the core idea and main steps of Bresenham's line algorithm when drawing a 2D thin line? (Please list 6 basic steps)**
**3. Write out the 4×4 transformation matrices with homogeneous coordinates for the following two geometric transformations:**
(A) Rotation by angle $\theta$ around the y-axis.
(B) Translation along the vector $v=(t_x, t_y, t_z)$.
**4. In the clipping stage, the Cohen-Sutherland line clipping algorithm uses 4-bit code-words. Please write down the specific criteria for "trivial accept" and "trivial reject" in this algorithm.**
**5. Please list the main differences between parallel projection and perspective projection, and state one major visual advantage of perspective projection over parallel projection.**
**6. What are the three main illumination components in the Phong Illumination Model? Please write down their names and briefly explain their meanings.**
**7. The Z-buffering (or depth-buffering) method is currently one of the most popular hidden surface removal algorithms. Please briefly describe its basic working principle.**
**8. Please list the main stages involved in the rendering pipeline in sequential order.**
**9. Rasterization rendering and ray tracing are two different rendering approaches. Briefly describe the basic tracing direction of the ray tracing algorithm, and list one of its main advantages and one of its main disadvantages.**
**10. What specific illumination phenomenon is the radiosity algorithm designed to handle that ray tracing cannot? Are its computed results view-dependent or view-independent?**

---

### Reference Answers
**1. Briefly describe two main advantages and two main disadvantages of Polygon Meshes as a representation of 3D objects.**

- **Answer:**
  - **Advantages:** (1) Extremely flexible and can represent complex details; (2) Easy to modify (e.g., smoothing, subdivision, and deformation); (3) High rendering processing efficiency.
  - **Disadvantages:** (1) Resolution-limited, meaning high details require dense meshes which increase memory and computational overhead; (2) Inherent error exists since planar surfaces are used to approximate curved surfaces; (3) Complex topology makes it difficult to handle non-manifold edges and holes.
**2. What are the core idea and main steps of Bresenham's line algorithm when drawing a 2D thin line? (Please list 6 basic steps)**

- **Answer:**
  1. Set x to $x_1$, y to $y_1$, and shade this pixel.
  2. Increase x by 1, and correspondingly $y = y + m$.
  3. Compute D1 - the distance of $(x, y)$ from the center of the upper pixel.
  4. Compute D2 - the distance of $(x, y)$ from the center of the lower pixel.
  5. If $D1 < D2$ (i.e., the line is closer to the upper pixel), shade the upper pixel; otherwise, shade the lower pixel.
  6. If the endpoint $(x_2, y_2)$ is not achieved, return to step 2; otherwise, stop.
**3. Write out the 4×4 transformation matrices with homogeneous coordinates for the following two geometric transformations:**

- **Answer:**
(A) Rotation by angle $\theta$ around the y-axis:
$R_y = \begin{bmatrix} cos\theta & 0 & sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -sin\theta & 0 & cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$
(B) Translation along the vector $v=(t_x, t_y, t_z)$:
$T = \begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}$
**4. In the clipping stage, the Cohen-Sutherland line clipping algorithm uses 4-bit code-words. Please write down the specific criteria for "trivial accept" and "trivial reject" in this algorithm.**

- **Answer:**
  - **Trivial accept:** If both endpoint codes are "0000" (i.e., the bitwise OR of the two codes is 0), the line is completely inside the clipping region and is accepted.
  - **Trivial reject:** If both endpoint codes have a 1 in the same bit position (i.e., the bitwise AND of the two codes is not 0), the line is completely outside the same boundary and is rejected.
**5. Please list the main differences between parallel projection and perspective projection, and state one major visual advantage of perspective projection over parallel projection.**

- **Answer:**
  - **Differences:** In parallel projection, the center of projection (COP) is at infinity, all projectors are parallel, and parallelism is preserved. In perspective projection, the COP is at a finite distance, all projectors meet at the COP, and parallelism is not preserved in general.
  - **Advantage of perspective projection:** It gives us depth information (foreshortening), creating a realistic visual effect where objects further away appear smaller.
**6. What are the three main illumination components in the Phong Illumination Model? Please write down their names and briefly explain their meanings.**

- **Answer:**
  1. **Ambient reflection (Ia​):** A uniform light intensity that illuminates objects equally from all directions, completely independent of the surface position and viewing angle.
  2. **Diffuse reflection (Id​):** Light reflected equally in all directions from a rough surface, where its intensity is proportional to the cosine of the angle between the light ray vector and the surface normal.
  3. **Specular reflection (Is​):** Handles highlights on smooth surfaces, where the intensity depends on the angle between the viewing vector and the reflection vector.
**7. The Z-buffering (or depth-buffering) method is currently one of the most popular hidden surface removal algorithms. Please briefly describe its basic working principle.**

- **Answer:**
The algorithm utilizes two buffers: a frame buffer (to store color) and a depth buffer (Z-buffer, to store the depth of the currently closest surface).
During processing, the depth of each pixel is calculated. If the depth is less than the current value stored in the Z-buffer (meaning the new surface is closer to the viewpoint), it updates the frame buffer with the new color and updates the Z-buffer with the new depth. Otherwise, the pixel is ignored.
**8. Please list the main stages involved in the rendering pipeline in sequential order.**

- **Answer:**
(1) Input object models
(2) World coordinate transformation
(3) Perspective transformation
(4) Back-face removal
(5) Clipping
(6) Rasterization
(7) Hidden surface removal and shading
*(Finally, Output image)*
**9. Rasterization rendering and ray tracing are two different rendering approaches. Briefly describe the basic tracing direction of the ray tracing algorithm, and list one of its main advantages and one of its main disadvantages.**

- **Answer:**
  - **Tracing direction:** It operates in a backward manner, tracing rays from the eye point (center of projection) through the pixels on the image plane into the scene to find intersections with objects.
  - **Advantage:** It can perfectly compute specular reflections, refractions, and accurate, clear shadows.
  - **Disadvantage:** It is extremely slow (high computational cost) and cannot compute indirect diffuse reflections (scattering between objects).
**10. What specific illumination phenomenon is the radiosity algorithm designed to handle that ray tracing cannot? Are its computed results view-dependent or view-independent?**

- **Answer:**
  - The radiosity algorithm is designed to accurately model **indirect diffuse reflections** (the light scattering between objects) within an entire scene.
  - The computed radiosity results are **view-independent**, because in diffuse reflection, the light energy is radiated uniformly in all directions regardless of where the camera is placed.