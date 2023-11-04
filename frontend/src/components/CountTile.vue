<template>
    <div v-if="Object.keys(tileResult).length" class="card card-container">
        <div class="card-body">
            <div class="movie-count-container p-1">
                <span class="movie-label">{{ tileResult['label'] }}</span>
                <span class="movie-label">{{ tileResult['value'] }} </span>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'CountTile',
    props: {
        tileResult: {
            type: Object
        }
    }
}
</script>

<style>
.movie-count-container {
    font-size: 21px;
}
.movie-label {
    margin: 0 0 0 2.5%;
    font-weight: 800;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}
</style>