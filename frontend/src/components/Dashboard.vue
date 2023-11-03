<template>
    <Line :data="data" :options="options"/>
</template>

<script>
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import {Line} from 'vue-chartjs'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

export default {
    name: 'DashboardViewer',
    components: {
        Line
    },
    data() {
        return {
            data: {
                labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                datasets: [
                    {
                        label: 'Data One',
                        backgroundColor: '#f87979',
                        pointRadius: 0,
                        tension: 0.3,
                        data: [40, 39, 10, 40, 39, 80, 40]
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        ticks: {
                            color: "#b6baca",
                        },
                        grid: {
                            drawTicks: false,
                        },
                        border: {
                            dash: [5, 10],
                        },
                    },
                    x: {
                        ticks: {
                            color: "#b6baca",
                        },
                        grid: {
                            display: false,
                        },
                        border: {
                            display: false,
                        },
                    },
                },
                interaction: {
                    intersect: false,
                },
                borderColor: "#c319ee",
                backgroundColor: "#c319ee",
            },
        }
    }
}
</script>