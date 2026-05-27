import React, {useEffect, useState} from 'react';
import axios from 'axios';

const API_URL = '';

export default function ReviewDashboard(){
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('authToken') || '');
  const [loginError, setLoginError] = useState('');

  useEffect(()=>{ fetchPending(); }, []);

  function authHeaders(){
    return token ? { Authorization: `Token ${token}` } : {};
  }

  function fetchPending(){
    setLoading(true);
    axios.get(`${API_URL}/api/emission-records/pending/`, { headers: authHeaders() })
      .then(r=>{ setRecords(r.data.results || r.data); setLoading(false); })
      .catch(()=> setLoading(false));
  }

  function doAction(id, action){
    axios.post(`${API_URL}/api/emission-records/${id}/${action}/`, {}, { headers: authHeaders() })
      .then(()=> fetchPending())
  }

  if(loading) return <div>Loading...</div>

  return (
    <div>
      <h2>Pending Records</h2>
      <div style={{marginBottom:16}}>
        <label>
          API token:
          <input value={token} onChange={e=>setToken(e.target.value)} style={{marginLeft:8,width:360}} />
        </label>
        <button type="button" onClick={() => { localStorage.setItem('authToken', token); setLoginError(''); fetchPending(); }} style={{marginLeft:8}}>Set token</button>
        {loginError && <span style={{color:'red', marginLeft:16}}>{loginError}</span>}
      </div>
      {records.length===0 && <div>No pending records</div>}
      <table style={{width:'100%',borderCollapse:'collapse'}}>
        <thead><tr><th>ID</th><th>Category</th><th>Amount</th><th>Unit</th><th>Period</th><th>Actions</th></tr></thead>
        <tbody>
          {records.map(r=> (
            <tr key={r.id} style={{borderTop:'1px solid #ddd'}}>
              <td>{r.id}</td>
              <td>{r.category}</td>
              <td>{r.amount}</td>
              <td>{r.unit}</td>
              <td>{r.start_date} {r.end_date?`- ${r.end_date}`:''}</td>
              <td>
                <button onClick={()=>doAction(r.id,'approve')}>Approve</button>
                <button onClick={()=>doAction(r.id,'reject')} style={{marginLeft:8}}>Reject</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
