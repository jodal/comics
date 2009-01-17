-- *** Database changes needed by the multi-release branch ***

-- Create release table
CREATE TABLE "comics_release" (
    "id" serial NOT NULL PRIMARY KEY,
    "comic_id" integer NOT NULL
    	REFERENCES "comics_comic" ("id")
	DEFERRABLE INITIALLY DEFERRED,
    "pub_date" date NOT NULL,
    "strip_id" integer NOT NULL
);

-- Add contraints to release table
ALTER TABLE "comics_release" ADD CONSTRAINT "strip_id_refs_id_211be2b6bc8157fe"
	FOREIGN KEY ("strip_id")
	REFERENCES "comics_strip" ("id")
	DEFERRABLE INITIALLY DEFERRED;

-- Add indexes to release table
CREATE INDEX "comics_release_comic_id" ON "comics_release" ("comic_id");
CREATE INDEX "comics_release_strip_id" ON "comics_release" ("strip_id");

-- Set correct owner of release table
ALTER TABLE "comics_release" OWNER TO "comics";

-- Populate release table
INSERT INTO "comics_release" ("comic_id", "pub_date", "strip_id")
	SELECT "comic_id", "pub_date", "id" AS "strip_id" FROM "comics_strip";

-- Remove unimportant index on strip table
DROP INDEX "comics_strip_pub_date";

-- Drop pub_date column from strip table
ALTER TABLE "comics_strip" DROP COLUMN "pub_date";
