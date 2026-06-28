import { OpenAI } from "openai";
import { BaseMessage, ChatMessage, ContentBlock } from "@langchain/core/messages";

//#region src/utils/misc.d.ts
declare function messageToOpenAIRole(message: BaseMessage): OpenAI.ChatCompletionRole;
//#endregion
export { messageToOpenAIRole };
//# sourceMappingURL=misc.d.ts.map