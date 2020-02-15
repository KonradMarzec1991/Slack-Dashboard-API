const start = document.getElementById('start');
start.innerText = 'start';


const getJSON = () => {
    let p = new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/namespaces');
        xhr.responseType = 'json';

        xhr.onload = () => {
            resolve(xhr.response);
        };

        xhr.onerror = () => {
            reject(new Error('Something went wrong'));
        };

        xhr.send()
    });
    return p;
};


const renderHTML = arr => {
    arr.forEach(el => {
        console.log(el.name);
    })
};

getJSON().then(res => renderHTML(res));