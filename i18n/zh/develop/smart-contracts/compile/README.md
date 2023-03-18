# Build and Compile

Here is a list of libraries and repos to build your smart contract.

## Blueprint

### Overview

A development environment for TON blockchain for writing, testing, and deploying smart contracts. Read more in [Blueprint git repository](https://github.com/ton-community/blueprint).

### Installation

Run the following in terminal to create a new project and follow the on-screen instructions:

```console
npm create ton@latest
```

&nbsp;

### Features

* Create a development environment from template in one click - `npm create ton`
* Streamlined workflow for building, testing and deploying smart contracts
* Dead simple deployment to mainnet/testnet using your favorite wallet (eg. Tonkeeper)
* Blazing fast testing of multiple smart contracts in an isolated blockchain running in-process

### Tech stack

1. Compiling FunC with https://github.com/ton-community/func-js (no CLI)
2. Testing smart contracts with https://github.com/ton-community/sandbox
3. Deploying smart contracts with [TON Connect 2](https://github.com/ton-connect), [Tonhub wallet](https://tonhub.com/) or a `ton://` deeplink

### Requirements

* [Node.js](https://nodejs.org) with a recent version like v18, verify version with `node -v`
* IDE with TypeScript and FunC support like [Visual Studio Code](https://code.visualstudio.com/) with the [FunC plugin](https://marketplace.visualstudio.com/items?itemName=tonwhales.func-vscode)

### How to use?
* [Watch DoraHacks presentation with demo of working with blueprint](https://www.youtube.com/watch?v=5ROXVM-Fojo).
* Read well detailed explanation in [Blueprint repo](https://github.com/ton-community/blueprint#create-a-new-project).


## ton-compiler

### Overview

Packaged FunC compiler for TON smart contracts:
* GitHub: [ton-community/ton-compiler](https://github.com/ton-community/ton-compiler)
* NPM: [ton-compiler](https://www.npmjs.com/package/ton-compiler)

### Installation

```bash npm2yarn
npm install ton-compiler
```

### Features

* Multiple FunC compiler versions
* Doesn't need to install and compile TON
* Programmatic and CLI interfaces
* Ready to use in unit-testing

### How to use

This packages adds `ton-compiler` binary to a project.

FunC compilation is a multi-stage process. One is compiling Func to Fift code that is then compiled to a binary representation. Fift compiler already has Asm.fif bundled.

FunC stdlib is bundled but could be disabled at runtime.

#### Console Use

```bash
# Compile to binary form (for contract creation)
ton-compiler --input ./wallet.fc --output ./wallet.cell

# Compile to fift (useful for debuging)
ton-compiler --input ./wallet.fc --output-fift ./wallet.fif

# Compile to fift and fift
ton-compiler --input ./wallet.fc --output ./wallet.cell --output-fift ./wallet.fif

# Disable stdlib
ton-compiler --no-stdlib --input ./wallet.fc --output ./wallet.cell --output-fift ./wallet.fif

# Pick version
ton-compiler --version "legacy" --input ./wallet.fc --output ./wallet.cell --output-fift ./wallet.fif
```

#### Programmatic Use

```javascript
import { compileContract } from "ton-compiler";
let result = await compileContract({ code: 'source code', stdlib: true, version: 'latest' });
if (result.ok) {
  console.log(result.fift); // Compiled Fift assembler
  console.log(result.cell); // Compiled cell Buffer
} else {
  console.warn(result.logs); // Output logs
}
```

## func-js

### Overview

_Cross-platform_ bindings for TON FunC compiler.

It's more low-level than ton-compiler, so use it only if ton-compiler doesn't work for you.

* GitHub: [ton-community/func-js](https://github.com/ton-community/func-js)
* NPM: [@ton-community/func-js](https://www.npmjs.com/package/@ton-community/func-js)

### Installation

```bash npm2yarn
npm install @ton-community/func-js
```

### Features

* No need to compile of download FunC binaries
* Works both in Node.js & **WEB** (WASM support is required)
* Compiles straight to BOC with code Cell
* Assembly is returned fot debugging purposes
* Does not depend on file-system


### How to use

Internally, this package uses both FunC compiler and Fift interpreter combined to single lib compiled to WASM.

Simple schema:

```bash
(your code) -> WASM(FunC -> Fift -> BOC)
```

Sources to the internal lib could be found [here](https://github.com/ton-blockchain/ton/tree/testnet/crypto/funcfiftlib).

### Usage example

```javascript
import {compileFunc, compilerVersion} from '@ton-community/func-js';
import {Cell} from 'ton';

async function main() {
    // You can get compiler version 
    let version = await compilerVersion();
    
    let result = await compileFunc({
        // Entry points of your project
        entryPoints: ['main.fc'],
        // Sources
        sources: {
            "stdlib.fc": "<stdlibCode>",
            "main.fc": "<contractCode>",
            // Rest of the files which are included in main.fc if some
        }
    });

    if (result.status === 'error') {
        console.error(result.message)
        return;
    }

    // result.codeBoc contains base64 encoded BOC with code cell 
    let codeCell = Cell.fromBoc(Buffer.from(result.codeBoc, "base64"))[0];
    
    // result.fiftCode contains assembly version of your code (for debug purposes)
    console.log(result.fiftCode)
}
```

Note that all FunC source file contents used in your project should be passed to `sources`, including:

* entry points
* stdlib.fc (if you use it)
* all files included in entry points


### Validated by TON Community

* [ton-community/ton-compiler](/develop/smart-contracts/sdk/javascript#ton-compiler) — ready-to-use FunC compiler for TON smart contracts.
* [ton-community/func-js](/develop/smart-contracts/sdk/javascript#func-js) — cross-platform bindings for the TON FunC compiler.

### Third-party contributors

* [grozzzny/ton-compiler-groz](https://github.com/grozzzny/ton-compiler-groz) — TON FunC smart contract compiler.
* [Termina1/tonc](https://github.com/Termina1/tonc) — TONC (TON Compiler). Uses WASM, so perfect for Linux.


## Other

* [disintar/toncli](https://github.com/disintar/toncli) — one of the most popular approaches. You even can use it with Docker.
* [tonthemoon/ton](https://github.com/tonthemoon/ton) — _(closed beta)_ one-line TON binaries installer.
* [delab-team/tlbcrc](https://github.com/delab-team/tlbcrc) — Package & CLI to generate opcodes by TL-B scheme