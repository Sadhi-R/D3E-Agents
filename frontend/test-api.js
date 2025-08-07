const testFrontendAPI = async () => {
    try {
        console.log('Testing frontend API communication...');
        
        // Test 1: Check if backend is reachable directly
        const directResponse = await fetch('http://localhost:8001/api/projects');
        console.log('Direct API call status:', directResponse.status);
        
        // Test 2: Check via proxy (how frontend calls it)
        const proxyResponse = await fetch('/api/projects');
        console.log('Proxy API call status:', proxyResponse.status);
        
        // Test 3: Test AI generation endpoint
        const aiResponse = await fetch('/api/ai/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: 'Create a simple test widget',
                project: 'Syllabus Management'
            })
        });
        console.log('AI generation call status:', aiResponse.status);
        const aiData = await aiResponse.json();
        console.log('AI response:', aiData);
        
    } catch (error) {
        console.error('API test failed:', error);
    }
};

// Run the test
testFrontendAPI();
