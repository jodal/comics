Spec-001: Multiple releases of a single comic strip
===================================================

*Spec created:*
    2009-01-17
*Spec implemented:*
    2009-01-17


Goals
-----

- When a comic releases old strips anew:

  - do not add a new strip, but instead
  - add a new release of the strip, so that
  - the strip is displayed as the comic's strip for both the old and the new
    release date.


Data model changes
------------------

This spec requires changes to the data model:

- Addition of a ``has_reruns`` boolean field to the ``Comic`` model.
- Addition of a new ``Release`` model.
- Removal of the ``pub_date`` field from the ``Strip`` model to the ``Release``
  model.

The following is an upgrade script for PostgreSQL:

.. code-block:: sql

    -- Add has_reruns column to comic table
    ALTER TABLE "comics_comic"
        ADD COLUMN "has_reruns" boolean NOT NULL DEFAULT false;

    -- Create release table
    CREATE TABLE "comics_release" (
        "id" serial NOT NULL PRIMARY KEY,
        "comic_id" integer NOT NULL
            REFERENCES "comics_comic" ("id")
            DEFERRABLE INITIALLY DEFERRED,
        "pub_date" date NOT NULL,
        "strip_id" integer NOT NULL
    );

    -- Add constraints to release table
    ALTER TABLE "comics_release"
        ADD CONSTRAINT "strip_id_refs_id_211be2b6bc8157fe"
            FOREIGN KEY ("strip_id")
            REFERENCES "comics_strip" ("id")
            DEFERRABLE INITIALLY DEFERRED;

    -- Add indexes to release table
    CREATE INDEX "comics_release_comic_id" ON "comics_release" ("comic_id");
    CREATE INDEX "comics_release_strip_id" ON "comics_release" ("strip_id");
    CREATE INDEX "comics_release_comic_id_pub_date_strip_id"
        ON "comics_release" ("comic_id", "pub_date", "strip_id");

    -- Set correct owner of release table
    ALTER TABLE "comics_release" OWNER TO "comics";

    -- Populate release table
    INSERT INTO "comics_release" ("comic_id", "pub_date", "strip_id")
        SELECT "comic_id", "pub_date", "id" AS "strip_id" FROM "comics_strip";

    -- Remove unimportant index on strip table
    DROP INDEX "comics_strip_pub_date";

    -- Drop pub_date column from strip table
    ALTER TABLE "comics_strip" DROP COLUMN "pub_date";
