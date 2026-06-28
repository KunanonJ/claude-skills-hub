let _langchain_core_runnables = require("@langchain/core/runnables");
let _langchain_core_tools = require("@langchain/core/tools");
let _langchain_core_singletons = require("@langchain/core/singletons");
//#region src/tools/custom.ts
function customTool(func, fields) {
	return new _langchain_core_tools.DynamicTool({
		...fields,
		description: "",
		metadata: { customTool: fields },
		func: async (input, runManager, config) => new Promise((resolve, reject) => {
			const childConfig = (0, _langchain_core_runnables.patchConfig)(config, { callbacks: runManager?.getChild() });
			_langchain_core_singletons.AsyncLocalStorageProviderSingleton.runWithConfig((0, _langchain_core_runnables.pickRunnableConfigKeys)(childConfig), async () => {
				try {
					resolve(func(input, childConfig));
				} catch (e) {
					reject(e);
				}
			});
		})
	});
}
//#endregion
exports.customTool = customTool;

//# sourceMappingURL=custom.cjs.map