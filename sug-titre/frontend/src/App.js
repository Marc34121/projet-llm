
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';


function App() {
  const [niche, setNiche] = useState("bricolage");
  const [videos, setVideos] =  useState([]);
  const [titres, setTitres] =  useState([]);
  const [formats, setFormats] =  useState([]);
  const [sujets, setSujets] =  useState([]);
  const [results, setResults] = useState([]);
  const [comments, setComments] =  useState([]);
  

const videosYoutube = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/videosYoutube`, {
      params: { niche: niche },
    });
    const fetched = res.data.videos || [];  // sécurité
    console.log("Contenu reçu:", res.data); //  diagnostic
    console.log("Type:", typeof res.data, "Array?", Array.isArray(res.data));
    setVideos(fetched);
    
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API :", error);
    setVideos([]); // au cas où pour éviter undefined
  }
};

const recupTitres = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/recupTitres`, {
      params: { niche: niche },
    });
    const fetched = res.data.titres || [];  // sécurité
    setTitres(fetched);
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API :", error);
    setTitres([]); // au cas où pour éviter undefined
  }
};

const recupFormats = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/recupFormats`, {
      params: { niche: niche },
    });
    const fetched = res.data.formats || [];  // sécurité
    setFormats(fetched);
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API :", error);
    setFormats([]); // au cas où pour éviter undefined
  }
};

const recupSujets = async () => {
  
    try {
    const res = await axios.get(`http://localhost:8000/recupSujets`, {
      params: { niche: niche ,top_n: 10 },
    });
    const fetched = res.data.sujets || [];  // sécurité
    console.log("Contenu reçu:", res.data); //  diagnostic
    console.log("Type:", typeof res.data.sujets, "Array?", Array.isArray(res.data.sujets));
    setSujets(fetched);
    
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API :", error);
    setSujets([]); // au cas où pour éviter undefined
  }
};

const recupIdees = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/recupIdees`, {
      params: { niche: niche },
    });
    const fetched = res.data || [];  // sécurité
    console.log("Contenu reçu:", res.data); //  diagnostic
    console.log("Type:", typeof res.data, "Array?", Array.isArray(res.data));
    setResults(fetched);
    
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API :", error);
    setResults([]); // au cas où pour éviter undefined
  }
};

const recupComments = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/recupComments`, {
      params: { niche: niche },
    });
    const fetched = res.data.comments || [];  // sécurité
    console.log("Contenu reçu:", res.data); //  diagnostic
    console.log("Type:", typeof res.data, "Array?", Array.isArray(res.data));
    setComments(fetched);
    
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API :", error);
    setComments([]); // au cas où pour éviter undefined
  }
};

  return (
    <div className="min-h-screen p-6 bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-4">Dashboard YouTube 📊</h1>

      {/* Choix de la niche */}
      <div className="mb-6">
        <label className="block mb-2">Choisis ta niche :</label>
        <select
          className="p-2 rounded text-black"
          value={niche}
          onChange={(e) => setNiche(e.target.value)}
        >
          <option value="gaming">Gaming</option>
          <option value="bricolage">Bricolage</option>
          <option value="cuisine">Cuisine</option>
        </select>
      </div>

      {/* Boutons */}
      <div className="flex flex-wrap gap-4 mb-8">
        <button onClick={videosYoutube} className="px-4 py-2 bg-green-500 rounded hover:bg-green-600">
          Charger titre
        </button>
        <button onClick={recupFormats} className="px-4 py-2 bg-purple-500 rounded hover:bg-purple-600">
          Charger Formats
        </button>
        <button onClick={recupSujets} className="px-4 py-2 bg-purple-500 rounded hover:bg-purple-600">
          Sujets tendances
        </button>
        <button onClick={recupComments} className="px-4 py-2 bg-purple-500 rounded hover:bg-purple-600">
          Voir commentaires
        </button>
        <button onClick={recupIdees} className="px-4 py-2 bg-purple-500 rounded hover:bg-purple-600">
          Générer Idées
        </button>
      </div>

      {/* Colonnes */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
     
        {/* Colonne 1 : IDs + titles */}
       {/* <div className="bg-gray-800 p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">IDs + Titres</h2>
          <ul className="space-y-2">
            {titres.map((video, index) => (
              <li key={index} className="bg-gray-700 p-3 rounded">
                {index + 1}. {video.id}-{video.title}
              </li>
            ))}
          </ul>
        </div> */}

        <div className="bg-gray-800 p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 text-white">IDs + Titres</h2>
              <ul className="space-y-2">
            {videos && videos.length > 0 ? (
              videos.map((video, index) => (
                <li key={video.id || index} className="bg-gray-700 p-3 rounded text-white">
                  {index + 1}. {video.id} — {video.title}
                </li>
                  ))
            ) : (
          <li className="text-gray-400 italic">Aucune vidéo disponible.</li>
            )}
              </ul>
        </div>
   

        {/* Colonne 2 : formats populaires */}
        <div className="bg-gray-800 p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Formats détectés</h2>
          <ul className="space-y-2">
            {formats.map((info, index) => (
              <li key={index} className="bg-gray-700 p-3 rounded">
                {index + 1}. {info}
              </li>
            ))}
          </ul>
        </div>
        
         {/* Colonne 3 : sujets tendances */}
         <div className="bg-gray-800 p-4 rounded-lg shadow">
           <h2 className="text-xl font-semibold mb-4">Sujets tendance</h2>
           <ul className="space-y-2">
            { sujets.map((sujet,index) => (
            <li key={index} className="bg-gray-700 p-3 rounded">
             {index + 1}.{sujet}</li>))}
           </ul>
         </div>
         
         {/* Colonne 4 : commentaires */}
        {Array.isArray(comments) && comments.length > 0 ? (
      comments.map((comment, index) => (
        <div
          key={index}
          className="bg-white rounded-2xl shadow-md p-4 border border-gray-100"
        >
          <p className="text-gray-800 text-sm">{comment}</p>
        </div>
      ))
        ) : (
          <p className="text-gray-400 italic">Aucun commentaire à afficher.</p>
        )}
       
  
  
        
        
        <div className="col-span-1 md:col-span-20 p-4 bg-gray-700 text-white">
        <p>{results.idees && results.idees.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">💡 Titres suggérés</h2>
          <ul className="list-disc list-inside space-y-1">
            {results.idees.map((idee, idx) => (
              <li key={idx}>{idee}</li>
            ))}
          </ul>
        </div>
      )}</p>
      </div>
        
      </div>
    </div>
  );

}

export default App;
