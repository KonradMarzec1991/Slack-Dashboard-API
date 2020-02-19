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
                let channelItem = document.createElement('li');
                channelItem.innerHTML = `${channel}`;
                channels.appendChild(channelItem);
            }
            htmlWorkspaces.appendChild(channels);
        }
        const sidebar = document.querySelector('.sidebar-content');
        sidebar.appendChild(htmlWorkspaces);
    }

    let tickets = res.list.tickets;

    const test = document.querySelector('.test');

    for (let ticket of tickets) {
        let ticketBody = document.createElement('div');
        ticketBody.classList.add('ticket');

        let ticketIcon = document.createElement('div');
        ticketIcon.classList.add('ticket-icon');

        let icon = document.createElement('i');
        icon.classList.add('far');
        icon.classList.add('fa-clipboard');

        ticketIcon.appendChild(icon);
        ticketBody.appendChild(ticketIcon);

        let ticketMain = document.createElement('div');
        ticketMain.classList.add('ticket-main');

        ticketBody.appendChild(ticketMain);
        let title = ticket.title;
        let description = ticket.description;

        let ticketTitle = document.createElement('h3');
        ticketTitle.innerHTML = `${title}`;
        let ticketDesc = document.createElement('p');
        ticketDesc.innerHTML = `${description}`;
        ticketDesc.classList.add('desc');

        ticketMain.appendChild(ticketTitle);
        ticketMain.appendChild(ticketDesc);

        let ticketProperties = document.createElement('div');
        ticketProperties.classList.add('ticket-properties');

        let iconEdit = document.createElement('i');
        iconEdit.classList.add('far');
        iconEdit.classList.add('fa-edit');

        let iconDelete = document.createElement('i');
        iconDelete.classList.add('far');
        iconDelete.classList.add('fa-trash-alt');

        ticketProperties.appendChild(iconEdit);
        ticketProperties.appendChild(iconDelete);
        ticketBody.appendChild(ticketProperties);

        test.appendChild(ticketBody);
    }

});