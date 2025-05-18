/*
 * sudoku.js
 * written by Conrad Shyu (conradshyu@yahoo.com)
 * last updated on 12/26/2020
*/
const unique = (v, i, self) => {
    return(self.indexOf(v) === i);
}   // return unique values within in array

const shuffle = (a, b) => {
    return(Math.random() > 0.5 ? -1 : 1);
}   // randomly shuffle elements in array

// b: values to replace
function place(a, b, v, fx) {
    let j = 0; let r = [];

    for (let i = 0; i < a.length; ++i) {
        r.push(fx(a[i], v) ? b[j++] : a[i]);
    }   // replace values in array

    return(r);
}   // place elements in second to first array

// a: values to be removed
function remove(b, a) {
    let r = [];

    for (let i = 0; i < b.length; ++i) {
        if (a.includes(b[i])) {
            continue;
        }   // skip the duplicate value

        r.push(b[i]);
    }   // save unique values

    return(r);
}   // remove identical elements

function permutation(a) {
    let r = [];

    if (a.length < 2) {
        return(JSON.parse(JSON.stringify(a)));
    };  // need more than 2 elements

    for (let i = 0; i < a.length; i++) {
        const x = a[i];
        const y = permutation(a.slice(0, i).concat(a.slice(i + 1)));

        for (let j = 0; j < y.length; j++) {
            r.push([x].concat(y[j]));
        }
    }

    return(r);
}   // calculate permutations

function check_column(m, r) {
    for (let i = 0; i < 9; ++i) {
        let a = [];

        for (let j = 0; j < r; ++j) {
            a.push(m[j][i]);
        }   // collect numbers in column

        a = remove(a, [0]);     // remove zeros from array

        if (a.filter(unique).length < a.length) {
            return(false);
        }   // duplicate numbers found
    }   // check unique numbers in column

    return(true);
}   // check unique numbers in column

function check_block(m, r) {
    for (let i = 0; i < 9; i += 3) {
        for (let j = (Math.floor((r - 1) / 3) * 3); j < r; j += 3) {
            let a = [];
            a = a.concat((m[j]).slice(i, i + 3));
            a = ((j + 1) < r) ? a.concat((m[j + 1]).slice(i, i + 3)) : a;
            a = ((j + 2) < r) ? a.concat((m[j + 2]).slice(i, i + 3)) : a;
            a = remove(a, [0]);     // remove zeros from array

            if (a.filter(unique).length < a.length) {
                return(false);
            }   // duplicate numbers found
        }   // concatenate array
    }   // check unique numbers in block

    return(true);
}   // check unique numbers in block

function puzzle(m, p = 0.5) {
    for (let i = 0; i < m.length; ++i) {
        for (let j = 0; j < m[i].length; ++j) {
            m[i][j] = (Math.random() < p) ? 0 : m[i][j];
        }
    }   // randomly remove some numbers

    return(m);
}   // generate a puzzle

function solve(m) {
    found = false; let q = [];

    while (!found) {
        q = JSON.parse(JSON.stringify(m));

        for (let r = 0; r < q.length; ++r) {
            let a = JSON.parse(JSON.stringify(q[r]));   // save a copy
            let d = remove([1, 2, 3, 4, 5, 6, 7, 8, 9], q[r]);

            if (d.length == 0) {
                found = true; continue;
            }   // row has already been filled

            let p = (d.length > 1) ? permutation(d) : [d];
            p.sort(shuffle); found = false;

            for (let x = 0; x < p.length; ++x) {
                q[r] = place(JSON.parse(JSON.stringify(a)), p[x], 0,
                    (x, y) => {return((x == y) ? true : false);});

                if (check_column(q, 9) && check_block(q, r + 1)) {
                    found = true; break;
                }   // solution found
            }

            if (!found) {
                break;
            }   // no solution can be found
        }
    }   // run until solution is found

    return(q);
}   // solve sudoku matrix

function run() {
    let found = false;
    let matrix = [[1, 2, 3, 4, 5, 6, 7, 8, 9]];
    let p = permutation([1, 2, 3, 4, 5, 6, 7, 8, 9]);

    while (!found) {
        (matrix[0]).sort(shuffle);       // shuffle the first row

        for (let i = 1; i < 9; ++i) {
            found = false; p.sort(shuffle);

            for (let j = 0; j < p.length; ++j) {
                matrix[i] = p[j];

                if (check_column(matrix, i + 1) && check_block(matrix, i + 1)) {
                    found = true; break;
                }   // success, found suitable permutation
            }

            if (!found) {
                break;
            }   // duplicate numbers found
        }   // construct the matrix
    }   // rerun if deadlock has been detected

    return(matrix);
}   // generate sudoku matrix

// main function
(() => {
    for (let i = 0; i < 2; ++i) {
        let m = run();      // generate a sudoku matrix

        console.log("** Complete Sudoku Matrix");
        for (let j = 0; j < m.length; ++j) {
            console.log(JSON.stringify(m[j]));
        }   // print out the original matrix

        console.log("       -----       ");
        console.log("** Sudoku Puzzle");
        let q = puzzle(JSON.parse(JSON.stringify(m)), 0.5);

        for (let j = 0; j < q.length; ++j) {
            console.log(JSON.stringify(q[j]));
        }   // print out the puzzle matrix

        console.log("       -----       ");
        console.log("** Sudoku Solution");
        let s = solve(JSON.parse(JSON.stringify(q)));

        for (let j = 0; j < s.length; ++j) {
            console.log(JSON.stringify(s[j]));
        }   // print out the solution matrix

        console.log("       *****       ");
    }   // print sudoku matrix
})();
