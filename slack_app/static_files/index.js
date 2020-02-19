

const getJSON = () => {
    let p = new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/namespaces/1/tickets/');
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

// Create workspace / channel hierarchy

getJSON().then(res => {
    let workspaces = res.workspace;
    let htmlWorkspaces = document.createElement('ul');
    htmlWorkspaces.classList.add('sidebar-workspace');

    for (let key of Object.keys(workspaces)) {
        let workspace = document.createElement('li');
        workspace.innerHTML = `${key}`;
        htmlWorkspaces.appendChild(workspace);

        if (typeof workspaces[key] == 'object') {
            let channels = document.createElement('ul');
            channels.classList.add('sidebar-channels');
            htmlWorkspaces.appendChild(channels);

            for (let channel of workspaces[key]) {
                console.log(channel);
                let channelItem = document.createElement('li');
                channelItem.innerHTML = `${channel}`;
                channels.appendChild(channelItem);
            }
            htmlWorkspaces.appendChild(channels);
        }
        const sidebar = document.querySelector('.sidebar-content');
        sidebar.appendChild(htmlWorkspaces);
    }

});