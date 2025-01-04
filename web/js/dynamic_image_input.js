import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.DynamicImageCombiner",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // 检查是否为 DynamicImageCombiner 节点
        if (nodeData.name === "DynamicImageCombiner") {
            // 保存原始的 onNodeCreated 方法
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // 重写 onNodeCreated 方法
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                // 初始化连接计数器
                this.lastConnectedCount = 0;
                // 添加第一个图像输入
                this.addInput("image_1", "IMAGE");
                return result;
            };

            // 处理连接变化的方法
            nodeType.prototype.onConnectionsChange = function(connectionType, slot, isConnected) {
                // 只处理输入连接的变化
                if (connectionType === 1) {
                    // 计算当前已连接的图像输入数量
                    const connectedCount = this.inputs.reduce((count, input) => 
                        input.name.startsWith('image_') ? (count + (input.link ? 1 : 0)) : count, 0);

                    // 如果连接数量发生变化
                    if (connectedCount !== this.lastConnectedCount) {
                        this.lastConnectedCount = connectedCount;
                        const targetCount = Math.max(connectedCount + 1, 1); // 确保至少保留一个输入

                        // 获取所有image输入
                        const imageInputs = this.inputs
                            .map((input, index) => ({ index, name: input.name }))
                            .filter(input => input.name.startsWith('image_'));

                        // 添加新的输入槽位
                        if (imageInputs.length < targetCount) {
                            const newIndex = imageInputs.length + 1;
                            this.addInput(`image_${newIndex}`, "IMAGE");
                        }

                        // 只在确实需要移除时才移除多余的输入槽位
                        if (imageInputs.length > targetCount) {
                            // 从后向前检查未连接的输入
                            for (let i = imageInputs.length - 1; i >= targetCount; i--) {
                                const input = this.inputs[imageInputs[i].index];
                                if (!input.link) {
                                    this.removeInput(imageInputs[i].index);
                                }
                            }
                        }

                        // 更新节点大小和画布
                        this.setSize(this.computeSize());
                        app.graph.setDirtyCanvas(true);
                    }
                }
            };
        }
    }
});