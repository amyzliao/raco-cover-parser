from bs4 import BeautifulSoup
import os   

def parse_cover_html(path, row):
    file = open(path, "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')

    result = soup.find('div', class_='file-lines')
    lines = result.find_all('div', class_='line')

    covering = False
    covered_lines = 0
    total_lines = 0
    coverRanges = []
    rangeStart = None
    for i, line in enumerate(lines):
        if 'START_COVER' in line.text:
            covering = True
            rangeStart = i
        if 'FINISH_COVER' in line.text and covering:
            covering = False
            rangeEnd = i
            coverRanges.append([rangeStart, rangeEnd])
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
        'ranges of lines considered [start, stop]': coverRanges,
        'covered lines': covered_lines,
        'total lines': total_lines,
        'percent of lines covered': covered_lines/total_lines
    }

    return rowStats

def countTotalLines(path):
    file = open(path, "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')

    result = soup.find('div', class_='file-lines')
    lines = result.find_all('div', class_='line')

    covering = False
    total_lines = 0
    for i, line in enumerate(lines):
        if 'START_COVER' in line.text:
            covering = True
        if 'FINISH_COVER' in line.text and covering:
            covering = False
            break # may remove later
        if covering:
            covered = line.find_all('span', class_='covered')
            uncovered = line.find_all('span', class_='uncovered')
            if len(covered) > 0 or len(uncovered) > 0:
                # the line has some coverage or uncoverage (it's not irrelevant)
                total_lines += 1
    return total_lines

def parse_folder(folderPath):
    # get all the files inside the folder
    # also serves as map of index to test number
    filelist = os.listdir(folderPath)
    NUM_TESTS = len(filelist)
    # determine number of lines up for consideration
    NUM_LINES = countTotalLines(folderPath + filelist[0])
    # rows are tests, columns are lines
    # 0 indicates uncovered; 1 indicates covered
    lineCoverageMatrix = [[0 for i in range(NUM_LINES)] for i in range(NUM_TESTS)]
    # maps test number to index
    testToRow = {}
    # maps test index to stats
    statsMatrix = [None for i in range(NUM_TESTS)]

    for i,file in enumerate(filelist):
        testToRow[file] = i
        statsMatrix[i] = parse_cover_html(folderPath + file, lineCoverageMatrix[i])

    print('test to row')
    for key,value in testToRow.items():
        print('{ ', key, ': ', value, ' }')
    print('line coverage matrix')
    for i, row in enumerate(lineCoverageMatrix):
        print(i, row)
    print('stats matrix')
    for i, row in enumerate(statsMatrix):
        print(i, row)
    
parse_folder('../zombie-coverage/coverage-new/files-cover/')