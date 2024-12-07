function stupid_animate(width, height, container, vertex, edge) {
    console.log("Called the stupid animate function.")
    let scene, camera, renderer, orbit, dragControls;
    const nodes = [];
    const lines = [];

    // Sample input data            
    // const vertices = [
    //     [0, 0, 1],
    //     [0, 1, 0],
    //     [0, 0, -1],
    //     [1, 0, 0],
    //     [0,0,0]
    // ];

    // const edges = {
    //     0: [1, 2,3,4],
    //     1: [2, 3,4],
    //     2: [3,4],
    //     3: [4]
    // };
    const vertices = vertex;
    const edges = edge;

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf7dada);
        
        camera = new THREE.PerspectiveCamera(
            30,
            width / height,
            1,
            100
        );
        camera.position.z = 5;
        
        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(width, height);
        
        container.innerHTML = '';
        container.appendChild(renderer.domElement);

        // Add lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        
        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(10, 10, 10);
        scene.add(pointLight);

        // Create nodes (vertices)
        vertices.forEach(position => {
            const geometry = new THREE.SphereGeometry(0.1, 32, 32);
            const material = new THREE.MeshStandardMaterial({ 
                color: 0xff69b4,
                metalness: 0.3,
                roughness: 0.4
            });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(...position);
            scene.add(sphere);
            nodes.push(sphere);
        });

        // Create edges
        Object.entries(edges).forEach(([from, tos]) => {
            tos.forEach(to => {
                const points = [
                    new THREE.Vector3(...vertices[from]),
                    new THREE.Vector3(...vertices[to])
                ];
                const geometry = new THREE.BufferGeometry().setFromPoints(points);
                const material = new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 5 }); // Changed linewidth to 5
                const line = new THREE.Line(geometry, material);
                scene.add(line);
                lines.push({
                    line: line,
                    startNodeIndex: parseInt(from),
                    endNodeIndex: to
                });
            });
        });

        // Set up orbit controls
        orbit = new THREE.OrbitControls(camera, renderer.domElement);
        orbit.enableDamping = true;
        orbit.dampingFactor = 0.05;

        // Set up drag controls
        dragControls = new THREE.DragControls(nodes, camera, renderer.domElement);
        
        dragControls.addEventListener('dragstart', function () {
            orbit.enabled = false;
        });
        
        dragControls.addEventListener('dragend', function () {
            orbit.enabled = true;
        });
        
        dragControls.addEventListener('drag', updateEdges);

        // Handle window resizing
        window.addEventListener('resize', onWindowResize, false);
    }

    function updateEdges() {
        lines.forEach(({line, startNodeIndex, endNodeIndex}) => {
            const startNode = nodes[startNodeIndex];
            const endNode = nodes[endNodeIndex];
            
            const positions = line.geometry.attributes.position.array;
            
            // Update start point
            positions[0] = startNode.position.x;
            positions[1] = startNode.position.y;
            positions[2] = startNode.position.z;
            
            // Update end point
            positions[3] = endNode.position.x;
            positions[4] = endNode.position.y;
            positions[5] = endNode.position.z;
            
            line.geometry.attributes.position.needsUpdate = true;

            // Keep the size of the spheres constant
            startNode.scale.set(1, 1, 1); // Set to desired constant size
            endNode.scale.set(1, 1, 1);   // Set to desired constant size
        });
    }

    function onWindowResize() {
        const container = document.getElementById('graph-container');
        const rect = container.getBoundingClientRect();
        
        camera.aspect = rect.width / rect.height;
        camera.updateProjectionMatrix();
        renderer.setSize(rect.width, rect.height);
    }

    function animate() {
        requestAnimationFrame(animate);
        orbit.update();
        // renderer.render(scene, camera);
        return renderer.render(scene, camera);

    }

    function highlightNodes() {
        // Highlight nodes 1 and 2
        const highlightColor = 0xffff00; // Yellow color for highlighting
        nodes[1].material.color.set(highlightColor);
        nodes[2].material.color.set(highlightColor);
    }
    function reset(){
        const highlightColor = 0xff69b4;
        nodes.forEach(node => {
            node.material.color.set(highlightColor);
        });
    }

    init();
    animate();
}

