import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.DynamicImageCombiner",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "DynamicImageCombiner") {
            // 重写 onNodeCreated
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // 初始化状态
                this.lastConnectedCount = 0;
                
                // 添加第一个输入点
                console.log("初始化：添加第一个图像输入点");
                this.addInput("image_1", "IMAGE");
                
                return result;
            };

            // 添加连接监听
            nodeType.prototype.onConnectionsChange = function(connectionType, slot, isConnected) {
                if (connectionType === 1) {  // 输入连接
                    console.log(`连接变化 - 槽位: ${slot}, 已连接: ${isConnected}`);
                    
                    // 计算已连接的输入点数量
                    const connectedCount = this.inputs.reduce((count, input) => 
                        count + (input.link ? 1 : 0), 0);
                    
                    console.log(`当前连接数量: ${connectedCount}, 上次连接数量: ${this.lastConnectedCount}`);

                    // 只在连接数量发生变化时更新
                    if (connectedCount !== this.lastConnectedCount) {
                        this.lastConnectedCount = connectedCount;
                        const targetCount = connectedCount + 1;
                        console.log(`目标输入点数量: ${targetCount}`);

                        // 添加新的输入点
                        while (this.inputs.length < targetCount) {
                            const newIndex = this.inputs.length + 1;
                            console.log(`添加新输入点: image_${newIndex}`);
                            this.addInput(`image_${newIndex}`, "IMAGE");
                        }

                        // 移除多余的输入点，但至少保留一个
                        while (this.inputs.length > Math.max(targetCount, 1)) {
                            const lastInput = this.inputs[this.inputs.length - 1];
                            if (!lastInput.link) {
                                console.log(`移除输入点: ${this.inputs.length}`);
                                this.removeInput(this.inputs.length - 1);
                            }
                        }

                        // 更新节点大小
                        console.log(`更新节点大小，当前输入点数量: ${this.inputs.length}`);
                        this.setSize(this.computeSize());
                        app.graph.setDirtyCanvas(true);
                    }
                }
            };
        }
    }
}); 