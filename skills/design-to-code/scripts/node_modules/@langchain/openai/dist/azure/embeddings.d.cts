import { AzureOpenAIInput } from "../types.cjs";
import { OpenAIEmbeddings, OpenAIEmbeddingsParams } from "../embeddings.cjs";
import { ClientOptions, OpenAI } from "openai";

//#region src/azure/embeddings.d.ts
declare class AzureOpenAIEmbeddings extends OpenAIEmbeddings {
  azureOpenAIApiVersion?: string;
  azureOpenAIApiKey?: string;
  azureADTokenProvider?: () => Promise<string>;
  azureOpenAIApiInstanceName?: string;
  azureOpenAIApiDeploymentName?: string;
  azureOpenAIBasePath?: string;
  constructor(fields?: Partial<OpenAIEmbeddingsParams> & Partial<AzureOpenAIInput> & {
    verbose?: boolean; /** The OpenAI API key to use. */
    apiKey?: string;
    configuration?: ClientOptions;
    deploymentName?: string;
    openAIApiVersion?: string;
  });
  protected embeddingWithRetry(request: OpenAI.EmbeddingCreateParams): Promise<OpenAI.CreateEmbeddingResponse & {
    _request_id?: string | null;
  }>;
}
//#endregion
export { AzureOpenAIEmbeddings };
//# sourceMappingURL=embeddings.d.cts.map