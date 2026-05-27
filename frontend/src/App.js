import React from 'react';
import ReviewDashboard from './components/ReviewDashboard';
import IngestionPanel from './components/IngestionPanel';
 
function App(){
  return (
    <div style={{padding:20, maxWidth:1000, margin:'0 auto'}}>
      <h1>Breathe ESG Prototype</h1>
      <IngestionPanel />
      <ReviewDashboard />
    </div>
  )
}

export default App;
