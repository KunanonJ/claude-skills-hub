import "./dalle.js";
import { webSearch } from "./webSearch.js";
import { mcp } from "./mcp.js";
import { codeInterpreter } from "./codeInterpreter.js";
import { fileSearch } from "./fileSearch.js";
import { imageGeneration } from "./imageGeneration.js";
import { computerUse } from "./computerUse.js";
import { localShell } from "./localShell.js";
import { shell } from "./shell.js";
import { applyPatch } from "./applyPatch.js";
import { toolSearch } from "./toolSearch.js";
//#region src/tools/index.ts
const tools = {
	webSearch,
	mcp,
	codeInterpreter,
	fileSearch,
	imageGeneration,
	computerUse,
	localShell,
	shell,
	applyPatch,
	toolSearch
};
//#endregion
export { tools };

//# sourceMappingURL=index.js.map