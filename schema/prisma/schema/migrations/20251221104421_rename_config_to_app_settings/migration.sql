/*
  Warnings:

  - You are about to drop the `config` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
DROP TABLE "config";

-- CreateTable
CREATE TABLE "app_settings" (
    "id" SERIAL NOT NULL,
    "last_reset_quota_date" DATE,

    CONSTRAINT "app_settings_pkey" PRIMARY KEY ("id")
);
