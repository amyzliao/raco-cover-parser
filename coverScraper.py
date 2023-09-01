from bs4 import BeautifulSoup
import os

NUM_TESTS = 20
NUM_LINES = 293

def parse_cover_html(path, row):
    file = open(path, "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')

    result = soup.find('div', class_='file-lines')
    lines = result.find_all('div', class_='line')

    covering = False
    covered_lines = 0
    total_lines = 0
    for line in lines:
        if 'START_COVER' in line.text:
            covering = True
        if 'FINISH_COVER' in line.text:
            covering = False
            break # may remove later
        if covering:
            covered = line.find_all('span', class_='covered')
            uncovered = line.find_all('span', class_='uncovered')
            if len(covered) > 0 or len(uncovered) > 0:
                # the line has some coverage or uncoverage (it's not irrelevant)
                total_lines += 1
                if len(covered) >= len(uncovered):
                    # the line is covered
                    row[total_lines-1] = 1
                    covered_lines += 1

    rowStats = {
        'covered lines': covered_lines,
        'total lines': total_lines,
        'percent of lines covered': covered_lines/total_lines
    }

    return rowStats


def parse_folder(folderPath):
    # 0 indicates uncovered; 1 indicates covered
    lineCoverageMatrix = [[0 for i in range(NUM_LINES)] for i in range(NUM_TESTS)]
    # maps test number to index
    testToRow = {}
    # serves as map of index to test number
    filelist = os.listdir(folderPath)
    # maps test index to stats
    statsMatrix = [None for i in range(NUM_TESTS)]

    for i,file in enumerate(filelist):
        testToRow[file] = i
        statsMatrix[i] = parse_cover_html(folderPath + file, lineCoverageMatrix[i])

    print('test to row')
    print(testToRow)
    print('line coverage matrix')
    for row in lineCoverageMatrix:
        print(row)
    print('stats matrix')
    for row in statsMatrix:
        print(row)
    

parse_folder('../zombie-coverage/coverage-new/files-cover/')