from settings_testing import *

# Test runner with code coverage
TEST_RUNNER = 'comics.utils.test_runner.test_runner_with_coverage'
COVERAGE_MODULES = (
    'comics.common.context_processors',
    'comics.common.feeds',
    'comics.common.models',
    'comics.common.utils.comic_strips',
    'comics.common.utils.navigation',
    'comics.common.utils.time_frames',
    'comics.common.views',
    'comics.crawler.crawlers',
    'comics.crawler.supercrawler',
    'comics.crawler.utils.webparser',
    'comics.sets.feeds',
    'comics.sets.forms',
    'comics.sets.middleware',
    'comics.sets.models',
    'comics.sets.views',
    'comics.utils.disk_import',
    'comics.utils.hash',
)
