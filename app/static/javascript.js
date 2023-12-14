const basicAutocomplete = document.querySelector('#basic');
const data = ['Museum', 'Party', 'Restaurant', 'Concert', 'Architecture'];
const dataFilter = (value) => {
    return data.filter((item) => {
        return item.toLowerCase().startsWith(value.toLowerCase());
    });
};

new mdb.Autocomplete(basicAutocomplete, {
    filter: dataFilter
});

const locationAutocomplete = document.querySelector('#location');
const dataL = ['Madrid', 'Rome', 'Lisbon', 'Paris', 'London'];
const dataFilterL = (value) => {
    return dataL.filter((item) => {
        return item.toLowerCase().startsWith(value.toLowerCase());
    });
};

new mdb.Autocomplete(locationAutocomplete, {
    filter: dataFilterL
});