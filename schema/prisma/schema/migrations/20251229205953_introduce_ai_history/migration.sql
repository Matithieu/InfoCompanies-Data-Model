-- CreateTable
CREATE TABLE "spring_ai_chat_memory" (
    "id" SERIAL NOT NULL,
    "conversation_id" VARCHAR(36) NOT NULL,
    "content" TEXT NOT NULL,
    "type" VARCHAR(10) NOT NULL,
    "timestamp" TIMESTAMP NOT NULL,

    CONSTRAINT "spring_ai_chat_memory_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_conversation" (
    "id" SERIAL NOT NULL,
    "conversation_id" VARCHAR(36),
    "user_id" TEXT,

    CONSTRAINT "user_conversation_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "spring_ai_chat_memory_conversation_id_idx" ON "spring_ai_chat_memory"("conversation_id");

-- CreateIndex
CREATE UNIQUE INDEX "user_conversation_conversation_id_key" ON "user_conversation"("conversation_id");

-- AddForeignKey
ALTER TABLE "spring_ai_chat_memory" ADD CONSTRAINT "spring_ai_chat_memory_conversation_id_fkey" FOREIGN KEY ("conversation_id") REFERENCES "user_conversation"("conversation_id") ON DELETE RESTRICT ON UPDATE CASCADE;
