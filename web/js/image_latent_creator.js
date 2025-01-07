import { app } from "../../../scripts/app.js";
import { setupSizeNode } from "./image_size_base.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.ImageLatentCreator",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ImageLatentCreator") {
            setupSizeNode(nodeType, nodeData, app);
            
            // 添加连接处理
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                const result = onConnectionsChange?.apply(this, arguments);
                
                // 如果是 resolution 输出端口的连接变化
                if (index === 4) {
                    console.log("[ImageLatentCreator] Resolution connection changed:", {type, connected, link_info});
                }
                
                return result;
            };
        }
    }
}); 