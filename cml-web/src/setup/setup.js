import React from "react";
import { BASE_URL, PAGES } from "../config";
import { Button, message } from "antd";
import ClientsTable from "./ClientsTable";
import ClientModal from "./ClientModal";

function Setup({ setPage }) {
  const [clients, setClients] = React.useState(null);
  const [editedClient, setEditedClient] = React.useState(null);
  const [availableCommands, setAvailableCommands] = React.useState([]);

  const fetchClients = () => {
    fetch(`${BASE_URL}/clients`, { method: "GET" })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
      })
      .then(fetched => setClients(fetched));
  };

  const fetchAvailableCommands = () => {
    fetch(`${BASE_URL}/commands`, { method: "GET" })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
      })
      .then(fetched => setAvailableCommands(fetched.map(it => it.number)));
  };

  const deleteClient = client => {
    fetch(`${BASE_URL}/clients/${client.id}`, { method: "DELETE" })
      .then(() => {
        message.success("Deleted");
        fetchClients();
      })
      .catch(err => message.error("Delete error " + err));
  };

  const saveClient = async (client) => {
    try {
      console.log('Going to save client ', client)
      await fetch(`${BASE_URL}/clients/${editedClient.id}`, {
        method: "PUT",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(client)
      });
      message.success("Saved");
      fetchClients();
    } catch (err) {
      message.error("Save error " + err);
    }
    setEditedClient(null);
  };

  React.useEffect(() => {
    fetchClients();
    fetchAvailableCommands();
  }, []);

  return (
    <div style={{ width: '95vw' }}>
      {clients && (
        <ClientsTable
          clients={clients}
          deleteHandler={deleteClient}
          editHandler={client =>
            setEditedClient({ approved: false, ...client })
          }
        />
      )}
      <Button type="primary" onClick={() => setPage(PAGES.keypad)}>
        Back
      </Button>
      <ClientModal 
        client={editedClient} 
        onCancel={() => setEditedClient(null)} 
        availableCommands={availableCommands}
        saveHandler={saveClient}
        key={editedClient ? editedClient.id : -1}
      />
    </div>
  );
}

export default Setup;
