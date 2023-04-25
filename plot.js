import * as Plot from "@observablehq/plot";

Plot.plot({
    y: {
	grid: true,
	label: "↑ Unemployment (%)"
    },
    marks: [
	Plot.ruleY([0]),
	Plot.line(bls, {x: "date", y: "unemployment", z: "division"})
    ]
})
