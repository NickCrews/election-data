// ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
// ┃ ██████ ██████ ██████       █      █      █      █      █ █▄  ▀███ █       ┃
// ┃ ▄▄▄▄▄█ █▄▄▄▄▄ ▄▄▄▄▄█  ▀▀▀▀▀█▀▀▀▀▀ █ ▀▀▀▀▀█ ████████▌▐███ ███▄  ▀█ █ ▀▀▀▀▀ ┃
// ┃ █▀▀▀▀▀ █▀▀▀▀▀ █▀██▀▀ ▄▄▄▄▄ █ ▄▄▄▄▄█ ▄▄▄▄▄█ ████████▌▐███ █████▄   █ ▄▄▄▄▄ ┃
// ┃ █      ██████ █  ▀█▄       █ ██████      █      ███▌▐███ ███████▄ █       ┃
// ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
// ┃ Copyright (c) 2017, the Perspective Authors.                              ┃
// ┃ ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ ┃
// ┃ This file is part of the Perspective library, distributed under the terms ┃
// ┃ of the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). ┃
// ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
// copied from https://perspective.finos.org/block/?example=file

import perspective from "https://cdn.jsdelivr.net/npm/@finos/perspective@3.0.0/dist/cdn/perspective.js";
import { Octokit } from "https://esm.sh/octokit";

window.addEventListener("DOMContentLoaded", async function () {
    const worker = await perspective.worker();

    var dropArea = document.getElementById("drop-area");
    var input = document.getElementById("fileElem");

    dropArea.addEventListener("dragenter", () => {}, false);
    dropArea.addEventListener("dragleave", () => {}, false);
    dropArea.addEventListener("dragover", () => {}, false);
    dropArea.addEventListener("drop", (x) => console.log(x), false);

    ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ["dragenter", "dragover"].forEach(function (eventName) {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ["dragleave", "drop"].forEach(function (eventName) {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add("highlight");
    }

    function unhighlight() {
        dropArea.classList.remove("highlight");
    }

    // Add event listener for drop.
    dropArea.addEventListener("drop", handleDrop, false);

    // Add event listener for file change on `input`.
    input.addEventListener("change", function () {
        handleFiles(this.files);
    });

    // Handle files attached to the drop.
    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;

        handleFiles(files);
    }

    // Iterate over files and call upload on each.
    function handleFiles(files) {
        [...files].forEach(uploadFile);
    }

    // Remove the `dropArea` and replace it with a `<perspective-viewer>`.
    function loadData(data) {
        const parent = dropArea.parentElement;
        const psp = document.createElement("perspective-viewer");
        parent.removeChild(dropArea);
        parent.appendChild(psp);
        psp.load(worker.table(data));
    }

    function uploadFile(file) {
        let reader = new FileReader();
        let type;
        if (file.name.endsWith(".feather") || file.name.endsWith(".arrow")) {
            type = "arrow";
        } else if (file.name.endsWith(".parquet") || file.name.endsWith(".pq")) {
            type = "parquet";
        } else {
            type = "csv";
        }

        
        reader.onload = async function (fileLoadedEvent) {
            let data = fileLoadedEvent.target.result;
            if (type === "parquet") {
                data = await parquetToArrow(data);
            }
            loadData(data);
        };

        // Read the contents of the file - triggering the onload when finished.
        if (type === "arrow" || type === "parquet") {
            reader.readAsArrayBuffer(file);
        } else {
            reader.readAsText(file);
        }
    }

    // fetch parquet data from releases
    // const releases = await fetch("https://api.github.com/repos/NickCrews/election-data/releases");
    // const data = await releases.json();
    // console.log(data);
    // var releaseSelect = document.getElementById("releaseSelect");
    // releaseSelect.innerHTML = "";
    // data.forEach((release) => {
    //     var option = document.createElement("option");
    //     option.text = release.tag_name;
    //     var url = release.assets[0].url;
    //     // url = "https://cors-proxy.htmldriven.com/?url=" + url;
    //     option.value = url;
    //     console.log(option.value);
    //     releaseSelect.add(option);
    // });
    // var loadRelease = document.getElementById("loadRelease");
    // loadRelease.addEventListener("click", async function () {
    //     const selected = releaseSelect.options[releaseSelect.selectedIndex].value;
    //     const GITHUB_TOKEN = "github_pat_***";
    //     const octokit = new Octokit({ auth: GITHUB_TOKEN });
    //     const response = await fetch(selected, {
    //         headers: {
    //             Accept: "application/octet-stream",
    //             Authorization: "Bearer " + GITHUB_TOKEN,
    //             "X-GitHub-Api-Version": "2022-11-28",
    //             // "User-Agent": "",
    //         },
    //     });
    //     console.log(response);
    //     console.log(await response.text());

    //     // transform the parquet file to arrow
    //     const parquetData = await response.arrayBuffer();
    //     const arrowData = await parquetToArrow(parquetData);
    //     loadData(arrowData);
    // });
});

// from https://gist.github.com/mhkeller/855ca5c0a6582e4ead7d36e6f8169fdd
// const arrow = require("apache-arrow");
// import arrow from 'https://cdn.jsdelivr.net/npm/apache-arrow@17.0.0/+esm'
import {tableToIPC, Table} from 'https://cdn.jsdelivr.net/npm/apache-arrow@17.0.0/+esm'
// import apacheArrow from 'https://cdn.jsdelivr.net/npm/apache-arrow@17.0.0/+esm'
// const { parseRecordBatch } = require("arrow-js-ffi");
// import arrowJsFfi from 'https://cdn.jsdelivr.net/npm/arrow-js-ffi@0.4.2/+esm'
import {parseRecordBatch} from 'https://cdn.jsdelivr.net/npm/arrow-js-ffi@0.4.2/+esm'
// const { readParquet, wasmMemory } = require("parquet-wasm");
import wasmInit, { readParquet, wasmMemory } from 'https://cdn.jsdelivr.net/npm/parquet-wasm@0.6.1/+esm'
// import pa from 'https://cdn.jsdelivr.net/npm/parquet-wasm@0.6.1/+esm'

async function parquetToArrow(parquetData) {
    // A reference to the WebAssembly memory object.
    // Update this version to match the version you're using.
    const wasmUrl = "https://cdn.jsdelivr.net/npm/parquet-wasm@0.6.1/esm/parquet_wasm_bg.wasm";
    await wasmInit(wasmUrl);
	const WASM_MEMORY = wasmMemory();

    console.log(parquetData);
    console.log(Table);
    console.log(tableToIPC);
	const parquetUint8Array = new Uint8Array(parquetData);

	const wasmArrowTable = readParquet(parquetUint8Array).intoFFI();

	const recordBatches = [];
	for (let i = 0; i < wasmArrowTable.numBatches(); i++) {
		// Note: Unless you know what you're doing, setting `true` below is recommended to _copy_
		// table data from WebAssembly into JavaScript memory. This may become the default in the
		// future.
		const recordBatch = parseRecordBatch(
			WASM_MEMORY.buffer,
			wasmArrowTable.arrayAddr(i),
			wasmArrowTable.schemaAddr(),
			true
		);
		recordBatches.push(recordBatch);
	}

	const table = new Table(recordBatches);
	// const table = new apacheArrow.Table(recordBatches);
  
    // Skip this step converting it to bytes if you just want the table
	const ipcStream = tableToIPC(table, 'stream');
	// const ipcStream = apacheArrow.tableToIPC(table, 'stream');
	const bytes = Buffer.from(ipcStream, 'utf-8');

	// VERY IMPORTANT! You must call `drop` on the Wasm table object when you're done using it
	// to release the Wasm memory.
	// Note that any access to the pointers in this table is undefined behavior after this call.
	// Calling any `wasmArrowTable` method will error.
	wasmArrowTable.drop();

	return bytes;
}