import { app } from "../../../scripts/app.js";
import { setupSizeNode } from "./image_size_base.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.ImageSizeCreator",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ImageSizeCreator") {
            setupSizeNode(nodeType, nodeData, app);
        }
    }
}); 