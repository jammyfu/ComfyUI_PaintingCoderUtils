import { app } from "../../../scripts/app.js";
import { setupSizeNode } from "./image_size_base.js";

app.registerExtension({
    name: "PaintingCoder.ImageSizeCreator",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ImageSizeCreator" || nodeData.name === "PaintingCoder::ImageSizeCreator") {
            setupSizeNode(nodeType, nodeData, app);
        }
    }
}); 