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
                    // 计算当前已连接的输入数量
                    const connectedCount = this.inputs.reduce((count, input) => 
                        count + (input.link ? 1 : 0), 0);

                    // 如果连接数量发生变化
                    if (connectedCount !== this.lastConnectedCount) {
                        this.lastConnectedCount = connectedCount;
                        const targetCount = connectedCount + 1;

                        // 添加新的输入槽位
                        while (this.inputs.length < targetCount) {
                            const newIndex = this.inputs.length + 1;
                            this.addInput(`image_${newIndex}`, "IMAGE");
                        }

                        // 移除未使用的输入槽位
                        while (this.inputs.length > Math.max(targetCount, 1)) {
                            const lastInput = this.inputs[this.inputs.length - 1];
                            if (!lastInput.link) {
                                this.removeInput(this.inputs.length - 1);
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