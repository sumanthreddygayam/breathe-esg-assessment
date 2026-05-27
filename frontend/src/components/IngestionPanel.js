import React, { useState } from 'react';
import axios from 'axios';

const API_URL = '';

export default function IngestionPanel(){
  const [sourceType, setSourceType] = useState('sap_fuel');
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [tenantId, setTenantId] = useState('1');

  function handleSubmit(event){
    event.preventDefault();
    if(!file){
      setStatus('Choose a file first.');
      return;
    }
    setStatus('Uploading...');
    const form = new FormData();
    form.append('file', file);
    axios.post(`${API_URL}/api/upload-csv/?tenant_id=${tenantId}&source_type=${sourceType}`, form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then(r => setStatus(`Uploaded ${r.data.created.length} records.`))
    .catch(err => setStatus(`Upload failed: ${err?.response?.data?.detail || err.message}`));
  }

  return (
    <div style={{padding:16, border:'1px solid #ccc', borderRadius:8, marginBottom:24}}>
      <h2>Ingest Source Data</h2>
      <form onSubmit={handleSubmit}>
        <div style={{marginBottom:12}}>
          <label>Tenant ID: <input value={tenantId} onChange={e=>setTenantId(e.target.value)} style={{width:80, marginLeft:8}}/></label>
        </div>
        <div style={{marginBottom:12}}>
          <label>Source type:</label>
          <select value={sourceType} onChange={e=>setSourceType(e.target.value)} style={{marginLeft:8}}>
            <option value="sap_fuel">SAP Fuel</option>
            <option value="sap_procurement">SAP Procurement</option>
            <option value="utility_electricity">Utility Electricity</option>
            <option value="travel_export">Travel Export</option>
          </select>
        </div>
        <div style={{marginBottom:12}}>
          <input type="file" accept=".csv" onChange={e=>setFile(e.target.files[0])} />
        </div>
        <button type="submit">Upload CSV</button>
      </form>
      {status && <div style={{marginTop:12}}>{status}</div>}
    </div>
  );
}
