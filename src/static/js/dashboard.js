(function () {
    "use strict";

    function cssVar(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    }

    function parseJsonScript(id) {
        return JSON.parse(document.getElementById(id).textContent);
    }

    function integerYAxis() {
        return {
            labels: {
                formatter: function (value) {
                    return Math.round(value);
                },
            },
        };
    }

    function baseGrid() {
        return {
            borderColor: cssVar("--color-border"),
            strokeDashArray: 0,
        };
    }

    function initPriorityChart(data) {
        const colors = [cssVar("--color-accent"), cssVar("--color-secondary"), cssVar("--color-danger")];
        const chart = new ApexCharts(document.querySelector("#priority-chart"), {
            chart: { type: "bar", height: 300, toolbar: { show: false } },
            series: [{ name: "Incidents", data: data.series }],
            xaxis: { categories: data.labels },
            yaxis: integerYAxis(),
            colors: colors,
            plotOptions: {
                bar: {
                    distributed: true,
                    borderRadius: 4,
                    borderRadiusApplication: "end",
                    columnWidth: "55%",
                },
            },
            legend: { show: false },
            dataLabels: { enabled: true },
            grid: baseGrid(),
            tooltip: { shared: false, intersect: true },
        });
        chart.render();
    }

    function initStatusChart(data) {
        const colors = [cssVar("--color-secondary"), cssVar("--color-accent"), cssVar("--color-muted")];
        const chart = new ApexCharts(document.querySelector("#status-chart"), {
            chart: { type: "bar", height: 300, toolbar: { show: false } },
            series: [{ name: "Incidents", data: data.series }],
            xaxis: { categories: data.labels },
            yaxis: integerYAxis(),
            colors: colors,
            plotOptions: {
                bar: {
                    distributed: true,
                    borderRadius: 4,
                    borderRadiusApplication: "end",
                    columnWidth: "55%",
                },
            },
            legend: { show: false },
            dataLabels: { enabled: true },
            grid: baseGrid(),
            tooltip: { shared: false, intersect: true },
        });
        chart.render();
    }

    function initEquipmentChart(data) {
        const chart = new ApexCharts(document.querySelector("#equipment-chart"), {
            chart: { type: "bar", height: 300, toolbar: { show: false } },
            series: [{ name: "Incidents", data: data.series }],
            xaxis: {
                categories: data.labels,
                labels: { rotate: -45, trim: true },
            },
            yaxis: integerYAxis(),
            colors: [cssVar("--color-accent")],
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    borderRadiusApplication: "end",
                    columnWidth: "55%",
                },
            },
            legend: { show: false },
            dataLabels: { enabled: false },
            grid: baseGrid(),
            tooltip: { shared: false, intersect: true },
        });
        chart.render();
    }

    function initEvolutionChart(data) {
        const chart = new ApexCharts(document.querySelector("#evolution-chart"), {
            chart: {
                type: "line",
                height: 300,
                toolbar: { show: true, tools: { download: true, selection: false, pan: true } },
            },
            series: [{ name: "Incidents", data: data.month }],
            xaxis: { type: "datetime" },
            yaxis: integerYAxis(),
            colors: [cssVar("--color-accent")],
            stroke: { width: 2, curve: "straight" },
            markers: { size: 5, strokeWidth: 2, strokeColors: cssVar("--color-bg-alt") },
            dataLabels: { enabled: false },
            grid: baseGrid(),
            tooltip: { shared: true, intersect: false, x: { format: "yyyy-MM-dd" } },
        });
        chart.render();

        const controls = document.getElementById("evolution-controls");
        controls.addEventListener("click", function (event) {
            const button = event.target.closest("button[data-granularity]");
            if (!button) {
                return;
            }
            const granularity = button.dataset.granularity;
            if (!data[granularity]) {
                return;
            }
            chart.updateSeries([{ name: "Incidents", data: data[granularity] }]);
            controls.querySelectorAll("button").forEach(function (btn) {
                btn.classList.toggle("active", btn === button);
            });
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initPriorityChart(parseJsonScript("priority-chart-data"));
        initStatusChart(parseJsonScript("status-chart-data"));
        initEquipmentChart(parseJsonScript("equipment-chart-data"));
        initEvolutionChart(parseJsonScript("evolution-chart-data"));
    });
})();
