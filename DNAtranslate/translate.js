
var codonTable = {
    // DNA codon to amino acid mapping
    'TTT': 'F',
    'TTC': 'F',
    'TTA': 'L',
    'TTG': 'L',
    'TCT': 'S',
    'TCC': 'S',
    'TCA': 'S',
    'TCG': 'S',
    'TAT': 'Y',
    'TAC': 'Y',
    'TAA': '*',
    'TAG': '*',
    'TGT': 'C',
    'TGC': 'C',
    'TGA': '*',
    'TGG': 'W',
    'CTT': 'L',
    'CTC': 'L',
    'CTA': 'L',
    'CTG': 'L',
    'CCT': 'P',
    'CCC': 'P',
    'CCA': 'P',
    'CCG': 'P',
    'CAT': 'H',
    'CAC': 'H',
    'CAA': 'Q',
    'CAG': 'Q',
    'CGT': 'R',
    'CGC': 'R',
    'CGA': 'R',
    'CGG': 'R',
    'ATT': 'I',
    'ATC': 'I',
    'ATA': 'I',
    'ATG': 'M',
    'ACT': 'T',
    'ACC': 'T',
    'ACA': 'T',
    'ACG': 'T',
    'AAT': 'N',
    'AAC': 'N',
    'AAA': 'K',
    'AAG': 'K',
    'AGT': 'S',
    'AGC': 'S',
    'AGA': 'R',
    'AGG': 'R',
    'GTT': 'V',
    'GTC': 'V',
    'GTA': 'V',
    'GTG': 'V',
    'GCT': 'A',
    'GCC': 'A',
    'GCA': 'A',
    'GCG': 'A',
    'GAT': 'D',
    'GAC': 'D',
    'GAA': 'E',
    'GAG': 'E',
    'GGT': 'G',
    'GGC': 'G',
    'GGA': 'G',
    'GGG': 'G'
};

function translateDNA() {
    var dnaSequence = document.getElementById("dnaSequence").value.toUpperCase().trim();
    var aminoAcidSequence = "";

    // Loop through the DNA sequence, reading three bases (codon) at a time.
    for (var i = 0; i < dnaSequence.length; i += 3) {
        var codon = dnaSequence.substring(i, i + 3);
        var aminoAcid = codonTable[codon];

        if (aminoAcid === undefined) {
            // If the codon is not found in the table (e.g., incomplete or invalid codon), show an error message.
            aminoAcidSequence = "<span class='color-orange'>Error: DNA序列碱基个数必须是3的倍数。</span>";
            break;
        }

        if (aminoAcid === '*') {
            // Replace stop codons with "*"
            aminoAcidSequence += "*";
        } else {
            aminoAcidSequence += aminoAcid;
        }
    }

    // Display the translated amino acid sequence on the webpage.
    document.getElementById("resultAminoAcidSequence").innerHTML = aminoAcidSequence +
        " @Translated by ANTBDY Science & technology.";
}

var aaPropertyOne = {
    A: {
        aaMap: 71.03711,
        aaPI: 6.00
    },
    C: {
        aaMap: 103.00919,
        aaPI: 5.07
    },
    D: {
        aaMap: 115.02694,
        aaPI: 2.77
    },
    E: {
        aaMap: 129.04259,
        aaPI: 3.22
    },
    F: {
        aaMap: 147.06841,
        aaPI: 5.48
    },
    G: {
        aaMap: 57.02146,
        aaPI: 5.97
    },
    H: {
        aaMap: 137.05891,
        aaPI: 7.59
    },
    I: {
        aaMap: 113.08406,
        aaPI: 6.02
    },
    K: {
        aaMap: 128.09496,
        aaPI: 9.74
    },
    L: {
        aaMap: 113.08406,
        aaPI: 5.98
    },
    M: {
        aaMap: 131.04049,
        aaPI: 5.74
    },
    N: {
        aaMap: 114.04293,
        aaPI: 5.41
    },
    P: {
        aaMap: 97.05276,
        aaPI: 6.30
    },
    Q: {
        aaMap: 128.05858,
        aaPI: 5.65
    },
    R: {
        aaMap: 156.10111,
        aaPI: 10.76
    },
    S: {
        aaMap: 87.03203,
        aaPI: 5.68
    },
    T: {
        aaMap: 101.04768,
        aaPI: 5.60
    },
    V: {
        aaMap: 99.06841,
        aaPI: 5.96
    },
    W: {
        aaMap: 186.07931,
        aaPI: 5.89
    },
    Y: {
        aaMap: 163.06333,
        aaPI: 5.66
    }
};

function calculateMwAndPI() {
    calculateMw();
    calculatePI();
}

function calculateMw() {
    var protein = document.getElementById("proteinSequence").value.replace(/[^ACDEFGHIKLMNPQRSTVWY]/ig, "");

    var mw = 0;
    for (let i = 0; i < protein.length; i++) {
        mw += aaPropertyOne[protein[i]].aaMap;
    }
    mw = mw + 18.015;
    // mw = mw - (protein.length - 1) * 18.015;

    document.getElementById("mwResult").innerHTML = "该蛋白质的分子量（MW）: " + (mw.toFixed(0) / 1000) + " kDa";
}

function calculatePI() {
    var seq = document.getElementById("proteinSequence").value.toUpperCase();
    var totalPI = 0;
    var numAminoAcids = 0;

    for (var i = 0; i < seq.length; i++) {
        var aminoAcid = seq[i];
        if (aaPropertyOne.hasOwnProperty(aminoAcid)) {
            totalPI += aaPropertyOne[aminoAcid].aaPI;
            numAminoAcids++;
        }
    }

    if (numAminoAcids > 0) {
        var proteinPI = totalPI / numAminoAcids;
        document.getElementById("piResult").innerHTML = "等电点（PI）: " + proteinPI.toFixed(2);
    } else {
        document.getElementById("piResult").innerHTML = "输入的蛋白质序列无效，请检查后重新输入。";
    }
}



// 密码子解析

var preferredCodons = {
    human: {
        'A': ['GCT', 'GCC', 'GCA'], // Alanine
        'R': ['CGC', 'CGG', 'AGA', 'AGG'], // Arginine
        'N': ['AAT', 'AAC'], // Asparagine
        'D': ['GAT', 'GAC'], // Aspartic Acid
        'C': ['TGT', 'TGC'], // Cysteine
        'Q': ['CAG', 'CAA'], // Glutamine
        'E': ['GAG', 'GAA'], // Glutamic Acid
        'G': ['GGT', 'GGC', 'GGA', 'GGG'], // Glycine
        'H': ['CAT', 'CAC'], // Histidine
        'I': ['ATT', 'ATC'], // Isoleucine
        'L': ['TTG', 'CTT', 'CTC', 'CTG'], // Leucine
        'K': ['AAA', 'AAG'], // Lysine
        'M': ['ATG'], // Methionine (Start Codon)
        'F': ['TTT', 'TTC'], // Phenylalanine
        'P': ['CCT', 'CCC', 'CCA'], // Proline
        'S': ['TCT', 'TCC', 'TCA', 'AGT', 'AGC'], // Serine
        'T': ['ACT', 'ACC', 'ACA'], // Threonine
        'W': ['TGG'], // Tryptophan
        'Y': ['TAT', 'TAC'], // Tyrosine
        'V': ['GTT', 'GTC', 'GTG'], // Valine
        '*': ['TAA', 'TGA', 'TAG']
    },
    ecoli: {
        'A': ['GCG', 'GCA', 'GCC', 'GCT'],
        'R': ['CGT', 'CGC'],
        'N': ['AAT', 'AAC'],
        'D': ['GAT', 'GAC'],
        'C': ['TGT', 'TGC'],
        'Q': ['CAA', 'CAG'],
        'E': ['GAA', 'GAG'],
        'G': ['GGT', 'GGC'],
        'H': ['CAT', 'CAC'],
        'I': ['ATT', 'ATC'],
        'L': ['CTG', 'TTA', 'TTG'],
        'K': ['AAA', 'AAG'],
        'M': ['ATG'],
        'F': ['TTT', 'TTC'],
        'P': ['CCG', 'CCA', 'CCT'],
        'S': ['AGC', 'TCT', 'AGT', 'TCC'],
        'T': ['ACC', 'ACG', 'ACT'],
        'W': ['TGG'],
        'Y': ['TAT', 'TAC'],
        'V': ['GTT', 'GTC', 'GTA', 'GTG'],
        '*': ['TAA', 'TGA', 'TAG']
    },
    yeast: {
        'A': ['GCT', 'GCC', 'GCA'], // Alanine
        'R': ['CGT', 'AGA', 'AGG'], // Arginine
        'N': ['AAT', 'AAC'], // Asparagine
        'D': ['GAT', 'GAC'], // Aspartic Acid
        'C': ['TGT', 'TGC'], // Cysteine
        'Q': ['CAA', 'CAG'], // Glutamine
        'E': ['GAA', 'GAG'], // Glutamic Acid
        'G': ['GGT', 'GGA'], // Glycine
        'H': ['CAT', 'CAC'], // Histidine
        'I': ['ATT', 'ATC'], // Isoleucine
        'L': ['TTG', 'CTT', 'CTG'], // Leucine
        'K': ['AAA', 'AAG'], // Lysine
        'M': ['ATG'], // Methionine (Start Codon)
        'F': ['TTT', 'TTC'], // Phenylalanine
        'P': ['CCT', 'CCA'], // Proline
        'S': ['TCT', 'TCC', 'TCA'], // Serine
        'T': ['ACT', 'ACC', 'ACA'], // Threonine
        'W': ['TGG'], // Tryptophan
        'Y': ['TAT', 'TAC'], // Tyrosine
        'V': ['GTT', 'GTC', 'GTG'], // Valine
        '*': ['TAA', 'TGA', 'TAG']
    },
    bevs: {
        'A': ['GCT', 'GCC'], // Alanine
        'R': ['CGT', 'CGC', 'AGA', 'AGG'], // Arginine
        'N': ['AAT', 'AAC'], // Asparagine
        'D': ['GAT', 'GAC'], // Aspartic Acid
        'C': ['TGT', 'TGC'], // Cysteine
        'E': ['GAA', 'GAG'], // Glutamic Acid
        'Q': ['CAA', 'CAG'], // Glutamine
        'G': ['GGT', 'GGC', 'GGA'], // Glycine
        'H': ['CAT', 'CAC'], // Histidine
        'I': ['ATT', 'ATC'], // Isoleucine
        'L': ['TTG', 'CTT', 'CTC', 'CTG'], // Leucine
        'K': ['AAA', 'AAG'], // Lysine
        'M': ['ATG'], // Methionine
        'F': ['TTT', 'TTC'], // Phenylalanine
        'P': ['CCT', 'CCC', 'CCA'], // Proline
        'S': ['TCT', 'TCC', 'AGC'], // Serine
        'T': ['ACT', 'ACC', 'ACA', ], // Threonine
        'W': ['TGG'], // Tryptophan
        'Y': ['TAT', 'TAC'], // Tyrosine
        'V': ['GTT', 'GTC', 'GTG'], // Valine
        '*': ['TAA', 'TGA', 'TAG']
    },

    cho: {
        'A': ['GCT', 'GCC', 'GCA'], // Alanine
        'R': ['CGG', 'CGC', 'AGA', 'AGG'], // Arginine
        'N': ['AAT', 'AAC'], // Asparagine
        'D': ['GAT', 'GAC'], // Aspartic Acid
        'C': ['TGT', 'TGC'], // Cysteine
        'E': ['GAA', 'GAG'], // Glutamic Acid
        'Q': ['CAA', 'CAG'], // Glutamine
        'G': ['GGG', 'GGC', 'GGA'], // Glycine
        'H': ['CAT', 'CAC'], // Histidine
        'I': ['ATT', 'ATC'], // Isoleucine
        'L': ['TTG', 'CTT', 'CTC', 'CTG'], // Leucine
        'K': ['AAA', 'AAG'], // Lysine
        'M': ['ATG'], // Methionine
        'F': ['TTT', 'TTC'], // Phenylalanine
        'P': ['CCT', 'CCC', 'CCA'], // Proline
        'S': ['TCT', 'TCC', 'TCA', 'AGT', 'AGC'], // Serine
        'T': ['ACT', 'ACC', 'ACA', ], // Threonine
        'W': ['TGG'], // Tryptophan
        'Y': ['TAT', 'TAC'], // Tyrosine
        'V': ['GTT', 'GTC', 'GTG'], // Valine
        '*': ['TAA', 'TGA', 'TAG']
    }

};

function optimizeCodons() {
    $('.analysis-result').show()
    var proteinSeq = document.getElementById("proteinSeq").value.toUpperCase();
    var selectedSpecies = document.querySelector('input[name="species"]:checked').value;
    var dnaSequence = translateToDNA(proteinSeq, selectedSpecies);
    var gcContent = calculateGCContent(dnaSequence);

    while (gcContent < 45 || gcContent > 59) {
        dnaSequence = translateToDNA(proteinSeq, selectedSpecies);
        gcContent = calculateGCContent(dnaSequence);
    }

    displayResult(dnaSequence, gcContent);
}

function translateToDNA(proteinSeq, selectedSpecies) {
    var dnaSequence = '';
    for (var i = 0; i < proteinSeq.length; i++) {
        var aminoAcid = proteinSeq[i];
        var codons = preferredCodons[selectedSpecies][aminoAcid];
        var randomCodon = codons[Math.floor(Math.random() * codons.length)];
        dnaSequence += randomCodon;
    }
    return dnaSequence;
}

function calculateGCContent(dnaSequence) {
    var gcCount = 0;
    for (var i = 0; i < dnaSequence.length; i++) {
        if (dnaSequence[i] === 'G' || dnaSequence[i] === 'C') {
            gcCount++;
        }
    }
    return (gcCount / dnaSequence.length) * 100;
}

function displayResult(dnaSequence, gcContent) {
    var resultGCContent = document.getElementById("resultGCContent");
    var resultDNASequence = document.getElementById("resultDNASequence");
    resultGCContent.innerHTML = "GC含量: " + gcContent.toFixed(2) + "%";
    resultDNASequence.innerHTML = "DNA序列: " + dnaSequence;
}

// 多肽设计


var aaProperty = {
    A: {
        hydrophilicity: 0.8,
        AntigenIndex: 0.95
    },
    R: {
        hydrophilicity: 1.19,
        AntigenIndex: 0.80
    },
    N: {
        hydrophilicity: 1.58,
        AntigenIndex: 1.55
    },
    D: {
        hydrophilicity: 1.62,
        AntigenIndex: 1.15
    },
    C: {
        hydrophilicity: 1.98,
        AntigenIndex: 1.15
    },
    Q: {
        hydrophilicity: 1.68,
        AntigenIndex: 1.15
    },
    E: {
        hydrophilicity: 0.756,
        AntigenIndex: 0.45
    },
    G: {
        hydrophilicity: 0.80,
        AntigenIndex: -0.15
    },
    H: {
        hydrophilicity: 0.2,
        AntigenIndex: 0.3
    },
    I: {
        hydrophilicity: 0.167,
        AntigenIndex: 0.3
    },
    L: {
        hydrophilicity: -0.0444,
        AntigenIndex: -0.6
    },
    K: {
        hydrophilicity: -0.344,
        AntigenIndex: -0.6
    },
    M: {
        hydrophilicity: -0.311,
        AntigenIndex: -0.6
    },
    F: {
        hydrophilicity: -0.567,
        AntigenIndex: 0.25
    },
    P: {
        hydrophilicity: 0.0778,
        AntigenIndex: 0.35
    },
    S: {
        hydrophilicity: 0.0333,
        AntigenIndex: 0.35
    },
    T: {
        hydrophilicity: -0.4,
        AntigenIndex: 0.35
    },
    W: {
        hydrophilicity: -0.189,
        AntigenIndex: -0.6
    },
    Y: {
        hydrophilicity: 0.122,
        AntigenIndex: -0.6
    },
    V: {
        hydrophilicity: -0.0556,
        AntigenIndex: -0.6
    }
};

function designPeptides() {
    $('.analysis-result').show()
    var proteinSeq = document.getElementById("proteinSeq").value;
    var peptides = [];

    // Generate peptides of length 15
    var peptideLength = 15;
    for (var i = 0; i <= proteinSeq.length - peptideLength; i++) {
        var pep = proteinSeq.substring(i, i + peptideLength);
        var score = calculateScore(pep);
        peptides.push({
            sequence: pep,
            score: score,
            startPos: i + 1
        });
    }

    // Sort peptides by score in descending order
    peptides.sort((a, b) => b.score - a.score);

    // Display top 50 peptides
    displayTopPeptides(peptides.slice(0, 50));
}

function calculateScore(peptide) {
    var sum = 0;
    for (var i = 0; i < peptide.length; i++) {
        var aa = peptide[i];
        if (aaProperty.hasOwnProperty(aa)) {
            sum += aaProperty[aa].hydrophilicity + 2 * aaProperty[aa].AntigenIndex;
        }
    }
    var score = sum / peptide.length;
    return score;
}

function displayTopPeptides(topPeptides) {
    var table = document.getElementById("resultTable");
    table.innerHTML = "<tr><th>多肽排序</th><th>起始位置</th><th>多肽序列</th><th>多肽分值</th></tr>";

    for (var i = 0; i < topPeptides.length; i++) {
        var row = table.insertRow(i + 1);
        var rankCell = row.insertCell(0);
        var startPosCell = row.insertCell(1);
        var sequenceCell = row.insertCell(2);
        var scoreCell = row.insertCell(3);

        rankCell.innerHTML = (i + 1).toString();
        startPosCell.innerHTML = topPeptides[i].startPos;
        sequenceCell.innerHTML = topPeptides[i].sequence;
        scoreCell.innerHTML = topPeptides[i].score.toFixed(4);
    }
}


// 抗体标记计算


function calculateConcentration() {
    const reagentMass = parseFloat(document.getElementById("reagentMass").value);
    const molecularWeight = parseFloat(document.getElementById("molecularWeight").value);
    const solventVolume = parseFloat(document.getElementById("solventVolume").value);

    // 确保输入的值都是有效的数字
    if (isNaN(reagentMass) || isNaN(molecularWeight) || isNaN(solventVolume)) {
        alert("请输入有效的数字！");
        return;
    }
    $('.calculator-result:eq(0)').show()
    // 浓度计算公式：浓度（nM） = (试剂质量 / 试剂分子量) / (溶剂体积 / 1000) * 10^6
    const concentration = (reagentMass / molecularWeight) / (solventVolume / 1000) * 1e3;

    document.getElementById("result").innerText = `溶液浓度：${concentration.toFixed(2)} mM`;
}

function calculateVolume() {
    const reagentMass = parseFloat(document.getElementById("reagentMass1").value);
    const molecularWeight = parseFloat(document.getElementById("molecularWeight1").value);
    const concentration = parseFloat(document.getElementById("concentration1").value);

    // 确保输入的值都是有效的数字
    if (isNaN(reagentMass) || isNaN(molecularWeight) || isNaN(concentration)) {
        alert("请输入有效的数字！");
        return;
    }
    $('.calculator-result:eq(1)').show()
    // 浓度计算公式：浓度（µL） = (试剂质量 / 试剂分子量) / (溶液浓度 / 1000) * 10^6
    const solventVolume = (reagentMass / molecularWeight) / (concentration / 1000) * 1e3;

    document.getElementById("result1").innerText = `所需溶剂体积：${solventVolume.toFixed(2)} µL`;

    // 将浓度值填入标记物的浓度输入框
    document.getElementById("C").value = concentration.toFixed(2);
}

function manualInput() {
    // 取消自动填充的结果，允许手动输入
    document.getElementById("C").removeAttribute("readonly");
}

function calculateLabelingVolume() {

    const V1 = parseFloat(document.getElementById("V1").value);
    const C1 = parseFloat(document.getElementById("C1").value);
    const R = parseFloat(document.getElementById("R").value);
    const M = parseFloat(document.getElementById("M").value);
    const C = parseFloat(document.getElementById("C").value);

    // 确保输入的值都是有效的数字
    if (isNaN(V1) || isNaN(C1) || isNaN(R) || isNaN(M) || isNaN(C)) {
        alert("请输入有效的数字！");
        return;
    }
    $('.calculator-result:eq(2)').show()
    // 标记物体积计算公式：V = 10^6 * (V1 * C1 * R) / (M * C)
    const labelingVolume = 1e6 * (V1 * C1 * R) / (M * C);

    document.getElementById("labelingResult").innerText = `标记物所需体积：${labelingVolume.toFixed(2)} µL`;
}

// elisa计算

function calculateDilutions() {
    const startingConcentration = parseFloat(document.getElementById("startingConcentration").value);
    const concentrationUnit = document.getElementById("concentrationUnit").value;
    const dilutionFactor = parseFloat(document.getElementById("dilutionFactor").value);
    const dilutionTimes = parseInt(document.getElementById("dilutionTimes").value);
    $('.analysis-result').show()
    let currentConcentration = startingConcentration;
    let resultTableContent =
        "<tr><th style=\"border: 1px solid black;background:purple;color:white;\">稀释次数</th><th style=\"border: 1px solid black;background:purple;color:white;text-align:center;\">浓度值</th><th style=\"border: 1px solid black;background:purple;color:white;text-align:center;\">稀释倍数</th></tr>";

    for (let i = 0; i <= dilutionTimes; i++) {
        resultTableContent += "<tr>";
        resultTableContent += "<td style=\"border: 1px solid black;\">" + i + "</td>";

        currentdiltiontimes = Math.pow(dilutionFactor, i);

        if (currentConcentration < 1) {
            let currentUnit = concentrationUnit;
            let convertedConcentration = currentConcentration;
            while (convertedConcentration < 1 && currentUnit !== "fg/ml") {
                if (currentUnit === "mg/ml") {
                    currentUnit = "µg/ml";
                    convertedConcentration *= 1000;
                } else if (currentUnit === "µg/ml") {
                    currentUnit = "ng/ml";
                    convertedConcentration *= 1000;
                } else if (currentUnit === "ng/ml") {
                    currentUnit = "pg/ml";
                    convertedConcentration *= 1000;
                } else if (currentUnit === "pg/ml") {
                    currentUnit = "fg/ml";
                    convertedConcentration *= 1000;
                } else if (currentUnit === "M") {
                    currentUnit = "mM";
                    convertedConcentration *= 1000;
                } else if (currentUnit === "mM") {
                    currentUnit = "µM";
                    convertedConcentration *= 1000;
                } else if (currentUnit === "µM") {
                    currentUnit = "nm";
                    convertedConcentration *= 1000;
                } else {
                    currentUnit = "nm";
                    convertedConcentration *= 1000;
                }
            }

            resultTableContent += "<td style=\"border: 1px solid black;padding-left: 27px\">" +
                convertedConcentration.toFixed(3) + " " +
                currentUnit + "</td>";
        } else {
            resultTableContent += "<td style=\"border: 1px solid black; padding-left:27px\">" +
                currentConcentration.toFixed(3) + " " +
                concentrationUnit + "</td>";
        }

        resultTableContent += "<td style=\"border: 1px solid black; padding-left:27px\">" +
            currentdiltiontimes + "</td>";
        currentConcentration = currentConcentration / dilutionFactor;

        resultTableContent += "</tr>";
    }

    document.getElementById("resultTable").innerHTML = resultTableContent;
}
