import { OpenAI } from "openai";
import { BindToolsInput } from "@langchain/core/language_models/chat_models";
import { DynamicTool } from "@langchain/core/tools";
//#region src/utils/tools.d.ts
type OpenAIToolChoice = OpenAI.ChatCompletionToolChoiceOption | "any" | string;
type ResponsesToolChoice = NonNullable<OpenAI.Responses.ResponseCreateParams["tool_choice"]>;
type ChatOpenAIToolType = BindToolsInput | OpenAI.Chat.ChatCompletionTool | ResponsesTool;
type ResponsesTool = NonNullable<OpenAI.Responses.ResponseCreateParams["tools"]>[number];
//#endregion
export { ChatOpenAIToolType, OpenAIToolChoice, ResponsesTool, ResponsesToolChoice };
//# sourceMappingURL=tools.d.ts.map