<template>
    <div class="card m-0 p-0 filter-header">
        <h2 class="header-name p-3">MOVIE FAN</h2>
    </div>
    <div class="container dashboard-container" style="max-width: 95% !important;">
        <div class="row">
            <div class="col-6">
                <div class="card card-container">
                    <div class="card-body">
                        <div class="movie-count-container p-2">
                            <span class="movie-label">Total Number of Movies </span>
                            <span class="movie-label">Name of director </span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-3">
                <div class="card card-container">
                    <div class="card-body p-0">
                        <div class="row display-flex justify-content-center align-items-center m-auto">
                            <div class="col-10 p-4 filter-container">
                                <span class="filter-label">Director: </span>
                                <span class="filter-label">Name of director </span>
                            </div>
                            <div class="col-2 float-right p-0">
                                <div class="dropdown">
                                    <div class="dropdown-toggle filter-dropdown" id="dropdownMenuButton"
                                         data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    </div>
                                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                        <a class="dropdown-item" href="#">Action</a>
                                        <a class="dropdown-item" href="#">Another action</a>
                                        <a class="dropdown-item" href="#">Something else here</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-3">
                <div class="card card-container">
                    <div class="card-body p-0">
                        <div class="row display-flex justify-content-center align-items-center m-auto">
                            <div class="col-10 p-4 filter-container">
                                <span class="filter-label">Star: </span>
                                <span class="filter-label">Name of Star </span>
                            </div>
                            <div class="col-2 float-right p-0">
                                <div class="dropdown">
                                    <div class="dropdown-toggle filter-dropdown" id="dropdownMenuButton"
                                         data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    </div>
                                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                        <a class="dropdown-item" href="#">Action</a>
                                        <a class="dropdown-item" href="#">Another action</a>
                                        <a class="dropdown-item" href="#">Something else here</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row pt-5">
            <div class="col-6">
                <div class="card card-container">
                    <div class="card-body">
                        <Line :data="data" :options="options"/>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <div class="card card-container">
                    <div class="card-body">
                        <Line :data="data" :options="options"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
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
                        backgroundColor: '#F5D257',
                        borderColor: '#F5D257',
                        pointRadius: 4,
                        tension: 0.3,
                        data: [43440, 0, 10, 40, 39, 80, 40],
                        yAxisID: 'y',
                    },
                    {
                        label: 'Data Two',
                        backgroundColor: '#F5D257',
                        borderColor: '#F5D257',
                        pointRadius: 0,
                        tension: 0.3,
                        data: [40, 39, 1230, 45450, 3923, 80, 40],
                        yAxisID: 'y',
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        position: 'left',
                        ticks: {
                            color: "#b6baca",
                        },
                        grid: {
                            drawTicks: false,
                            color: '#999999'
                        },
                        border: {
                            dash: [2, 10]
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
                }
            },
        }
    }
}
</script>
<style>
.dashboard-container {
    margin-top: 4%;
}

.card-container {
    background-color: #2B2B2B;
    border: none;
}

.filter-header {
    background-color: #2B2B2B;
    border: none;
}

.header-name {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}

.filter-label {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}

.filter-dropdown {
    color: white;
    font-size: 20px;
}

.filter-container {
    border-right: 1px solid #3e3e3e;
}

.movie-count-container {

}

.movie-label {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}
</style>