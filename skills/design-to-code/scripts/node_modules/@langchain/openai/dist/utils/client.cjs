const require_errors = require("./errors.cjs");
let openai = require("openai");
let _langchain_core_errors = require("@langchain/core/errors");
//#region src/utils/client.ts
function _isOpenAIContextOverflowError(e) {
	if (String(e).includes("context_length_exceeded")) return true;
	if ("message" in e && typeof e.message === "string" && (e.message.includes("Input tokens exceed the configured limit") || e.message.includes("exceeds the context window") || e.message.includes("maximum context length"))) return true;
	return false;
}
function wrapOpenAIClientError(e) {
	if (!e || typeof e !== "object") return e;
	let error;
	if (e.constructor.name === openai.APIConnectionTimeoutError.name && "message" in e && typeof e.message === "string") {
		error = new Error(e.message);
		error.name = "TimeoutError";
	} else if (e.constructor.name === openai.APIUserAbortError.name && "message" in e && typeof e.message === "string") {
		error = new Error(e.message);
		error.name = "AbortError";
	} else if (_isOpenAIContextOverflowError(e)) error = _langchain_core_errors.ContextOverflowError.fromError(e);
	else if ("status" in e && e.status === 400 && "message" in e && typeof e.message === "string" && e.message.includes("tool_calls")) error = require_errors.addLangChainErrorFields(e, "INVALID_TOOL_RESULTS");
	else if ("status" in e && e.status === 401) error = require_errors.addLangChainErrorFields(e, "MODEL_AUTHENTICATION");
	else if ("status" in e && e.status === 429) error = require_errors.addLangChainErrorFields(e, "MODEL_RATE_LIMIT");
	else if ("status" in e && e.status === 404) error = require_errors.addLangChainErrorFields(e, "MODEL_NOT_FOUND");
	else error = e;
	return error;
}
//#endregion
exports.wrapOpenAIClientError = wrapOpenAIClientError;

//# sourceMappingURL=client.cjs.map