-- *** Database changes needed by the multi-release branch ***

-- Remove unimportant index
DROP INDEX "comics_strip_pub_date";

-- Create release table
CREATE TABLE "comics_release" (
    "id" serial NOT NULL PRIMARY KEY,
    "comic_id" integer NOT NULL
    	REFERENCES "comics_comic" ("id")
	DEFERRABLE INITIALLY DEFERRED,
    "pub_date" date NOT NULL
);
CREATE INDEX "comics_release_comic_id" ON "comics_release" ("comic_id");

-- Create strip release table
CREATE TABLE "comics_strip_releases" (
    "id" serial NOT NULL PRIMARY KEY,
    "strip_id" integer NOT NULL
    	REFERENCES "comics_strip" ("id")
	DEFERRABLE INITIALLY DEFERRED,
    "release_id" integer NOT NULL
    	REFERENCES "comics_release" ("id")
	DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("strip_id", "release_id")
);

-- Populate release table
INSERT INTO "comics_release" ("comic_id", "pub_date")
	SELECT "comic_id", "pub_date" FROM "comics_strip";

-- Populate strip release table
INSERT INTO "comics_strip_releases" ("strip_id", "release_id")
	SELECT "s"."id" AS "strip_id", "r"."id" AS "release_id"
	FROM "comics_strip" "s", "comics_release" "r"
	WHERE "s"."comic_id" = "r"."comic_id"
		AND "s"."pub_date" = "r"."pub_date";

-- Drop pub_date column from strip
ALTER TABLE "comics_strip" DROP COLUMN "pub_date";
