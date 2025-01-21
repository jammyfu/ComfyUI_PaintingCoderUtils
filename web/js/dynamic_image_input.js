import { app } from "/scripts/app.js";

app.registerExtension({
    name: "PaintingCoder.DynamicImageCombiner",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "DynamicImageCombiner" || nodeData.name === "PaintingCoder::DynamicImageCombiner") {
            // 保存原始的 onNodeCreated 方法
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // 重写 onNodeCreated 方法
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // 确保至少有一个输入点
                if (!this.inputs || this.inputs.length === 0) {
                    this.addInput("image_1", "IMAGE");
                }
                
                // 初始化连接计数器
                this.lastConnectedCount = 0;
                
                // 强制刷新节点
                this.setSize(this.computeSize());
                app.graph.setDirtyCanvas(true);
                
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
                        const targetCount = Math.max(connectedCount + 1, 1);

                        // 获取所有image输入
                        const imageInputs = this.inputs
                            .map((input, index) => ({ index, name: input.name }))
                            .filter(input => input.name.startsWith('image_'));

                        // 添加新的输入槽位
                        if (imageInputs.length < targetCount) {
                            const newIndex = imageInputs.length + 1;
                            this.addInput(`image_${newIndex}`, "IMAGE");
                        }

                        // 移除多余的未连接输入槽位
                        if (imageInputs.length > targetCount) {
                            for (let i = imageInputs.length - 1; i >= targetCount; i--) {
                                const input = this.inputs[imageInputs[i].index];
                                if (!input.link) {
                                    this.removeInput(imageInputs[i].index);
                                }
                            }
                        }

                        // 强制刷新节点
                        this.setSize(this.computeSize());
                        app.graph.setDirtyCanvas(true);
                    }
                }
            };
        }
    }
});