(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3011],{875:(e,s,t)=>{Promise.resolve().then(t.bind(t,1966))},1966:(e,s,t)=>{"use strict";t.r(s),t.d(s,{default:()=>i});var a=t(5155),d=t(2115);function i(){let[e,s]=(0,d.useState)([{id:1,name:"Test Restaurant 1",address:"123 Test St",city:"Test City",kosher_category:"dairy",short_description:"Test description 1"},{id:2,name:"Test Restaurant 2",address:"456 Test Ave",city:"Test City",kosher_category:"meat",short_description:"Test description 2"}]),[t,i]=(0,d.useState)(!1);return(0,d.useEffect)(()=>{console.log("Test page loaded"),console.log("Test data:",e)},[e]),(0,a.jsxs)("div",{className:"min-h-screen bg-white p-4",children:[(0,a.jsx)("h1",{className:"text-2xl font-bold mb-4",children:"Test Page"}),(0,a.jsxs)("div",{className:"mb-4",children:[(0,a.jsxs)("p",{children:["Loading state: ",t?"Loading...":"Not loading"]}),(0,a.jsxs)("p",{children:["Test data count: ",e.length]})]}),(0,a.jsx)("div",{className:"space-y-4",children:e.map(e=>(0,a.jsxs)("div",{className:"border p-4 rounded-lg",children:[(0,a.jsx)("h2",{className:"text-lg font-semibold",children:e.name}),(0,a.jsxs)("p",{className:"text-gray-600",children:[e.address,", ",e.city]}),(0,a.jsxs)("p",{className:"text-sm text-blue-600",children:["Kosher: ",e.kosher_category]}),(0,a.jsx)("p",{className:"text-sm text-gray-500",children:e.short_description})]},e.id))}),(0,a.jsx)("button",{onClick:()=>i(!t),className:"mt-4 px-4 py-2 bg-blue-500 text-white rounded",children:"Toggle Loading"})]})}}},e=>{e.O(0,[8441,5964,7358],()=>e(e.s=875)),_N_E=e.O()}]);