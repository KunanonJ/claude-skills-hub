import OpenAI$1 from "openai";
import { DynamicTool, ToolRunnableConfig } from "@langchain/core/tools";
import { RunnableFunc } from "@langchain/core/runnables";

//#region src/tools/custom.d.ts
type CustomToolFields = Omit<OpenAI$1.Responses.CustomTool, "type">;
declare function customTool(func: RunnableFunc<string, string, ToolRunnableConfig>, fields: CustomToolFields): DynamicTool<string>;
//#endregion
export { customTool };
//# sourceMappingURL=custom.d.cts.map