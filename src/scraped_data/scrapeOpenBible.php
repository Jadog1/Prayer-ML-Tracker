<?php
require_once __DIR__ . '/vendor/autoload.php';

use GuzzleHttp\Client;
use GuzzleHttp\Promise;
use Symfony\Component\DomCrawler\Crawler;

// Global vars 
$chunkSize = 60;
$client = new Client();
$booksOfTheBible = [
    // Old Testament
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
    "Ecclesiastes", "Song Of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    
    // New Testament
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
];
$booksKeyed = [];
$crossRefsCSV = fopen('cross-refs.csv', 'w');
if (!$crossRefsCSV) die ('There was an issue opening cross-refs.csv.');

readCsvLineByLine('niv.csv');
fclose($crossRefsCSV);

function readCsvLineByLine(string $fileName) {
    global $chunkSize, $client;

    if (!file_exists($fileName) || !is_readable($fileName)) {
        echo "The file $fileName does not exist or is not readable.";
        return;
    }

    $file = fopen($fileName, 'r');
    if (!$file) die ("Error opening $fileName.");
    $totalLines = countLines($fileName);

    $lineCount = 0;

    // Loop through the file in chunks.
    while (($line = fgetcsv($file)) !== false) {
        $asyncRequests[] = $client->getAsync(formatURL($line));
        $lines[] = $line;
        
        if (count($asyncRequests) >= $chunkSize) {
            $responses = Promise\utils::unwrap($asyncRequests);
            foreach ($responses as $key => $response) {
                processResponse($lines[$key], $response);
            }

            $lines = [];
            $asyncRequests = [];
            displayProgressBar($lineCount, $totalLines);
        }

        $lineCount++;
    }

    // Finish it up.
    if (count($asyncRequests)) {
        $responses = Promise\utils::unwrap($asyncRequests);
        foreach ($responses as $key => $response) {
            processResponse($lines[$key], $response);
            displayProgressBar($lineCount, $totalLines);
        }
    }
}

function formatURL(array $line) {
    global $booksOfTheBible;

    $verse = $line[2];
    $chapter = $line[1];
    $book = $booksOfTheBible[$line[0] - 1];

    return "https://www.openbible.info/labs/cross-references/search?q=$book+$chapter+$verse";
}

function processResponse(array $line, object $response) {
    $crawler = new Crawler((string) $response->getBody());
    $crawler->filterXPath('//div[contains(@class, "crossrefs")]/div[not(contains(@class, "crossref-verse"))]')->each(function (Crawler $node, $i) use ($line) {
        global $booksOfTheBible, $booksKeyed, $crossRefsCSV;

        // Gather reference data.
        $modifier = 0;
        $info = preg_split("/[\s:-]+/", $node->filterXPath('//h3')->text());

        if (intval($info[0])) { // Books that starts with a number. Eg. 1st Samuel.
            $info[0] = $info[0] . ' ' . $info[1];
            $modifier = 1;
        } else if (strtolower($info[0]) == 'song') { // Spicy sex poem.
            $info[0] = 'Song Of Solomon';
            $modifier = 2;
        }

        if (!($referenceBook = $booksKeyed[$info[0]] ?? false)) {
            $referenceBook = (string) (array_search($info[0], $booksOfTheBible) + 1);
            $booksKeyed[$info[0]] = (string) $referenceBook;
        }

        $referenceChapter = (string) $info[1 + $modifier];
        $referenceStartVerse = (string) $info[2 + $modifier];
        $referenceEndVerse = (string) ($info[3 + $modifier] ?? 0);
        $referenceText =  $node->filterXPath('//p')->text();

        $class = $node->attr('class');
        $referenceWeight = $class ? substr($class, -1) : '0';

        // Source data.
        $book = $line[0];
        $chapter = $line[1];
        $verse = $line[2];

        fputcsv($crossRefsCSV, [$book, $chapter, $verse, $referenceBook, $referenceChapter, $referenceStartVerse, $referenceEndVerse, $referenceText, $referenceWeight]);
    });
}

function countLines($fileName) {
    $lineCount = 0;
    $handle = fopen($fileName, "r");
    while(!feof($handle)){
        fgets($handle);
        $lineCount++;
    }

    fclose($handle);
    return $lineCount;
}

function displayProgressBar($current, $total, $barLength = 50) {
    $progress = ($current / $total);
    $filledLength = round($barLength * $progress);
    $bar = str_repeat('█', $filledLength) . str_repeat('-', $barLength - $filledLength);

    $percent = round($progress * 100, 2);
    echo "\r|$bar| $percent% Complete";
    if ($current === $total) echo "\n";
}
?>
