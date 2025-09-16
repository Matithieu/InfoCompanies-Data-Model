-- CreateEnum
CREATE TYPE "public"."Status" AS ENUM ('NOT_DONE', 'TO_DO', 'DONE');

-- CreateTable
CREATE TABLE "public"."city" (
    "id" SERIAL NOT NULL,
    "name" TEXT,

    CONSTRAINT "city_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."industry_sector" (
    "id" SERIAL NOT NULL,
    "name" TEXT,

    CONSTRAINT "industry_sector_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."legal_form" (
    "id" SERIAL NOT NULL,
    "name" TEXT,

    CONSTRAINT "legal_form_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."region" (
    "id" SERIAL NOT NULL,
    "name" TEXT,

    CONSTRAINT "region_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."companies" (
    "id" SERIAL NOT NULL,
    "company_name" TEXT,
    "siren_number" TEXT,
    "nic_number" TEXT,
    "legal_form" TEXT,
    "ape_code" TEXT,
    "ape_label" TEXT,
    "address" TEXT,
    "postal_code" TEXT,
    "department_number" TEXT,
    "department" TEXT,
    "city" TEXT,
    "region" TEXT,
    "trade_name" TEXT,
    "registration_date" DATE,
    "deregistration_date" DATE,
    "closing_date_2018_1" DATE,
    "revenue_2018_1" DOUBLE PRECISION,
    "turnover_2018_1" DOUBLE PRECISION,
    "closing_date_2018_2" DATE,
    "revenue_2018_2" DOUBLE PRECISION,
    "turnover_2018_2" DOUBLE PRECISION,
    "closing_date_2018_3" DATE,
    "revenue_2018_3" DOUBLE PRECISION,
    "turnover_2018_3" DOUBLE PRECISION,
    "closing_date_2019_1" DATE,
    "revenue_2019_1" DOUBLE PRECISION,
    "turnover_2019_1" DOUBLE PRECISION,
    "closing_date_2019_2" DATE,
    "revenue_2019_2" DOUBLE PRECISION,
    "turnover_2019_2" DOUBLE PRECISION,
    "closing_date_2019_3" DATE,
    "revenue_2019_3" DOUBLE PRECISION,
    "turnover_2019_3" DOUBLE PRECISION,
    "closing_date_2020_1" DATE,
    "revenue_2020_1" DOUBLE PRECISION,
    "turnover_2020_1" DOUBLE PRECISION,
    "closing_date_2020_2" DATE,
    "revenue_2020_2" DOUBLE PRECISION,
    "turnover_2020_2" DOUBLE PRECISION,
    "closing_date_2020_3" DATE,
    "revenue_2020_3" DOUBLE PRECISION,
    "turnover_2020_3" DOUBLE PRECISION,
    "closing_date_2021_1" DATE,
    "revenue_2021_1" DOUBLE PRECISION,
    "turnover_2021_1" DOUBLE PRECISION,
    "closing_date_2021_2" DATE,
    "revenue_2021_2" DOUBLE PRECISION,
    "turnover_2021_2" DOUBLE PRECISION,
    "closing_date_2021_3" DATE,
    "revenue_2021_3" DOUBLE PRECISION,
    "turnover_2021_3" DOUBLE PRECISION,
    "closing_date_2022_1" DATE,
    "revenue_2022_1" DOUBLE PRECISION,
    "turnover_2022_1" DOUBLE PRECISION,
    "closing_date_2022_2" DATE,
    "revenue_2022_2" DOUBLE PRECISION,
    "turnover_2022_2" DOUBLE PRECISION,
    "closing_date_2022_3" DATE,
    "revenue_2022_3" DOUBLE PRECISION,
    "turnover_2022_3" DOUBLE PRECISION,
    "closing_date_2023_1" DATE,
    "revenue_2023_1" DOUBLE PRECISION,
    "turnover_2023_1" DOUBLE PRECISION,
    "closing_date_2023_2" DATE,
    "revenue_2023_2" DOUBLE PRECISION,
    "turnover_2023_2" DOUBLE PRECISION,
    "closing_date_2023_3" DATE,
    "revenue_2023_3" DOUBLE PRECISION,
    "turnover_2023_3" DOUBLE PRECISION,
    "industry_sector" TEXT,
    "phone_number" TEXT,
    "website" VARCHAR(3000),
    "reviews" JSONB,
    "schedule" JSONB,
    "instagram" VARCHAR(10000),
    "facebook" VARCHAR(3000),
    "twitter" VARCHAR(3000),
    "linkedin" VARCHAR(3000),
    "youtube" VARCHAR(3000),
    "email" VARCHAR(3000),
    "scraping_date" DATE,
    "date_creation" DATE,
    "last_processing_date" DATE,
    "number_of_employee" INTEGER,
    "company_category" TEXT,

    CONSTRAINT "companies_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."config" (
    "id" SERIAL NOT NULL,
    "last_reset_quota_date" DATE,

    CONSTRAINT "config_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."leaders" (
    "id" SERIAL NOT NULL,
    "siren" TEXT,
    "role" TEXT,
    "last_name" TEXT,
    "first_name" TEXT,
    "gestion_number" TEXT,
    "type" TEXT,
    "event_name" TEXT,
    "usage_name" TEXT,
    "pseudo" TEXT,
    "company_name" VARCHAR(3000),
    "legal_form" TEXT,
    "id_data" TEXT,

    CONSTRAINT "leaders_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."user_company_status" (
    "id" SERIAL NOT NULL,
    "user_id" TEXT,
    "status" "public"."Status",
    "company_id" INTEGER,

    CONSTRAINT "user_company_status_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."user_quota" (
    "user_id" TEXT NOT NULL,
    "quota_allocated" INTEGER,
    "quota_used" INTEGER,

    CONSTRAINT "user_quota_pkey" PRIMARY KEY ("user_id")
);

-- CreateIndex
CREATE INDEX "ix_city_name" ON "public"."city"("name");

-- CreateIndex
CREATE INDEX "ix_industry_sector_name" ON "public"."industry_sector"("name");

-- CreateIndex
CREATE INDEX "ix_legal_form_name" ON "public"."legal_form"("name");

-- CreateIndex
CREATE INDEX "ix_region_name" ON "public"."region"("name");

-- CreateIndex
CREATE INDEX "ix_companies_siren_number" ON "public"."companies"("siren_number");

-- CreateIndex
CREATE INDEX "ix_companies_company_name" ON "public"."companies"("company_name");

-- CreateIndex
CREATE INDEX "ix_companies_legal_form" ON "public"."companies"("legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_industry_sector" ON "public"."companies"("industry_sector");

-- CreateIndex
CREATE INDEX "ix_companies_region" ON "public"."companies"("region");

-- CreateIndex
CREATE INDEX "ix_companies_city" ON "public"."companies"("city");

-- CreateIndex
CREATE INDEX "ix_companies_phone_number" ON "public"."companies"("phone_number");

-- CreateIndex
CREATE INDEX "ix_companies_website" ON "public"."companies"("website");

-- CreateIndex
CREATE INDEX "ix_companies_email" ON "public"."companies"("email");

-- CreateIndex
CREATE INDEX "ix_companies_number_of_employee" ON "public"."companies"("number_of_employee");

-- CreateIndex
CREATE INDEX "ix_companies_linkedin" ON "public"."companies"("linkedin");

-- CreateIndex
CREATE INDEX "ix_companies_twitter" ON "public"."companies"("twitter");

-- CreateIndex
CREATE INDEX "ix_companies_facebook" ON "public"."companies"("facebook");

-- CreateIndex
CREATE INDEX "ix_companies_instagram" ON "public"."companies"("instagram");

-- CreateIndex
CREATE INDEX "ix_companies_youtube" ON "public"."companies"("youtube");

-- CreateIndex
CREATE INDEX "ix_companies_region_city_industry_sector_legal_form" ON "public"."companies"("region", "city", "industry_sector", "legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_region_city_industry_sector" ON "public"."companies"("region", "city", "industry_sector");

-- CreateIndex
CREATE INDEX "ix_companies_region_city_legal_form" ON "public"."companies"("region", "city", "legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_region_city" ON "public"."companies"("region", "city");

-- CreateIndex
CREATE INDEX "ix_companies_region_industry_sector" ON "public"."companies"("region", "industry_sector");

-- CreateIndex
CREATE INDEX "ix_companies_region_legal_form" ON "public"."companies"("region", "legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_city_industry_sector_legal_form" ON "public"."companies"("city", "industry_sector", "legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_city_industry_sector" ON "public"."companies"("city", "industry_sector");

-- CreateIndex
CREATE INDEX "ix_companies_city_legal_form" ON "public"."companies"("city", "legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_region_industry_sector_legal_form" ON "public"."companies"("region", "industry_sector", "legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_industry_sector_legal_form" ON "public"."companies"("industry_sector", "legal_form");

-- CreateIndex
CREATE INDEX "ix_companies_industry_sector_number_of_employee" ON "public"."companies"("industry_sector", "number_of_employee");

-- CreateIndex
CREATE INDEX "idx_leader_siren" ON "public"."leaders"("siren");

-- CreateIndex
CREATE INDEX "idx_leader_company_name" ON "public"."leaders"("company_name");

-- CreateIndex
CREATE INDEX "idx_leader_first_name" ON "public"."leaders"("first_name");

-- CreateIndex
CREATE INDEX "idx_leader_last_name" ON "public"."leaders"("last_name");

-- CreateIndex
CREATE INDEX "idx_leader_role" ON "public"."leaders"("role");

-- CreateIndex
CREATE INDEX "ix_user_company_status_user_id" ON "public"."user_company_status"("user_id");

-- CreateIndex
CREATE INDEX "ix_user_company_status_company_id" ON "public"."user_company_status"("company_id");

-- CreateIndex
CREATE INDEX "ix_user_quota_user_id" ON "public"."user_quota"("user_id");

-- CreateIndex
CREATE INDEX "ix_user_quota_quota_allocated" ON "public"."user_quota"("quota_allocated");

-- CreateIndex
CREATE INDEX "ix_user_quota_quota_used" ON "public"."user_quota"("quota_used");

-- AddForeignKey
ALTER TABLE "public"."user_company_status" ADD CONSTRAINT "user_company_status_company_id_fkey" FOREIGN KEY ("company_id") REFERENCES "public"."companies"("id") ON DELETE SET NULL ON UPDATE CASCADE;
