function stupid_animate(width, height, container, vertex, edge, names) {
    let scene, camera, renderer, orbit, dragControls;
    const nodes = [];
    const lines = [];
    const nodeLabels = [];

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

        // Add toggle button for names
        const toggleButton = document.createElement('button');
        toggleButton.textContent = 'label';
        toggleButton.style.position = 'absolute';
        toggleButton.style.right = '14px';
        toggleButton.style.size = 'bold';
        toggleButton.style.backgroundColor = '#1DA1F2';
        toggleButton.style.top = '10px';
        toggleButton.style.color = 'white';
        toggleButton.style.border = 'none';
        toggleButton.style.zIndex = '1000';
        toggleButton.addEventListener('mouseover', () => {
            toggleButton.style.transform = 'scale(1.1)';
        });

        toggleButton.addEventListener('mouseout', () => {
            toggleButton.style.transform = 'scale(1)';
        });
        container.appendChild(toggleButton);

        toggleButton.addEventListener('click', () => {
            nodeLabels.forEach(text => {
                if (text) {
                    text.visible = !text.visible;
                }
            });
        });

        // Create nodes (vertices)
        for (let i = 0; i < vertices.length; i++) {
            const position = vertices[i];
            const geometry = new THREE.SphereGeometry(0.1, 32, 32);
            const material = new THREE.MeshStandardMaterial({ 
                color: 0xff69b4,
                metalness: 0.3,
                roughness: 0.4
            });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(...position);
            sphere.name = names[i];
            // scene.add(new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.TextureLoader().load('https://i.imgur.com/6ZuOaXa.png'), transparent: true, opacity: 1 })));
            // const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.TextureLoader().load('https://i.imgur.com/6ZuOaXa.png'), transparent: true, opacity: 0 }));
            // sprite.position.copy(sphere.position);
            // sprite.position.y += 0.2;
            // sprite.scale.set(0.1, 0.1, 0.1);
            // scene.add(sprite);
            const loader = new THREE.FontLoader();
            loader.load('https://rawcdn.githack.com/mrdoob/three.js/r128/examples/fonts/helvetiker_bold.typeface.json', function (font) {
                const textGeometry = new THREE.TextGeometry(names[i], {
                    font: font,
                    size: 0.08,
                    color: "black",
                    height: 0.01,
                    curveSegments: 12,
                });
                const textMaterial = new THREE.MeshBasicMaterial({ color: "black" });
                const text = new THREE.Mesh(textGeometry, textMaterial);
                text.position.copy(sphere.position);
                text.position.y += 0.1;
                // Make text always face the camera
                text.rotation.set(0, 0, 0);
                text.quaternion.copy(camera.quaternion);
                scene.add(text);
                nodeLabels[i] = text;
            });
            scene.add(sphere);
            nodes.push(sphere);
        }

        // Create edges
        Object.entries(edges).forEach(([from, tos]) => {
            tos.forEach(to => {
                // Create the line
                const points = [
                    new THREE.Vector3(...vertices[from]),
                    new THREE.Vector3(...vertices[to])
                ];
                const geometry = new THREE.BufferGeometry().setFromPoints(points);
                const material = new THREE.LineBasicMaterial({ color: 0x000000 });
                const line = new THREE.Line(geometry, material);
                scene.add(line);

                // Create arrow head with smaller dimensions
                const direction = new THREE.Vector3(
                    vertices[to][0] - vertices[from][0],
                    vertices[to][1] - vertices[from][1],
                    vertices[to][2] - vertices[from][2]
                ).normalize();

                const arrowPosition = new THREE.Vector3(
                    vertices[to][0] - direction.x * 0.15,
                    vertices[to][1] - direction.y * 0.15,
                    vertices[to][2] - direction.z * 0.15
                );

                const arrowGeometry = new THREE.ConeGeometry(0.03, 0.1, 8);
                const arrowMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
                const arrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
                arrow.position.copy(arrowPosition);

                // Point the arrow in the right direction
                const quaternion = new THREE.Quaternion();
                quaternion.setFromUnitVectors(
                    new THREE.Vector3(0, 1, 0), 
                    direction
                );
                arrow.setRotationFromQuaternion(quaternion);

                scene.add(arrow);

                lines.push({
                    line: line,
                    arrow: arrow,
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
        
        dragControls.addEventListener('drag', function(event) {
            updateEdges();
            // Update text position
            const nodeIndex = nodes.indexOf(event.object);
            if (nodeIndex !== -1 && nodeLabels[nodeIndex]) {
                nodeLabels[nodeIndex].position.copy(event.object.position);
                nodeLabels[nodeIndex].position.y += 0.1;
            }
        });

        // Handle window resizing
        window.addEventListener('resize', onWindowResize, false);
    }

    function updateEdges() {
        lines.forEach(({line, arrow, startNodeIndex, endNodeIndex}) => {
            const startNode = nodes[startNodeIndex];
            const endNode = nodes[endNodeIndex];
            
            const positions = line.geometry.attributes.position.array;
            
            // Update line positions
            positions[0] = startNode.position.x;
            positions[1] = startNode.position.y;
            positions[2] = startNode.position.z;
            
            positions[3] = endNode.position.x;
            positions[4] = endNode.position.y;
            positions[5] = endNode.position.z;
            
            line.geometry.attributes.position.needsUpdate = true;

            // Update arrow position and rotation
            const direction = new THREE.Vector3(
                endNode.position.x - startNode.position.x,
                endNode.position.y - startNode.position.y,
                endNode.position.z - startNode.position.z
            ).normalize();

            const arrowPosition = new THREE.Vector3(
                endNode.position.x - direction.x * 0.2,
                endNode.position.y - direction.y * 0.2,
                endNode.position.z - direction.z * 0.2
            );

            arrow.position.copy(arrowPosition);

            const quaternion = new THREE.Quaternion();
            quaternion.setFromUnitVectors(
                new THREE.Vector3(0, 1, 0), 
                direction
            );
            arrow.setRotationFromQuaternion(quaternion);
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
        // Update text orientations to face camera
        nodeLabels.forEach(text => {
            if (text) {
                text.quaternion.copy(camera.quaternion);
            }
        });
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

