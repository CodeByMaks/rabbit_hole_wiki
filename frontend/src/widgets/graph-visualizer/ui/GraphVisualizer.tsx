// src/widgets/graph-visualizer/ui/GraphVisualizer.tsx
import { useGraphStore } from '../model/use-graph-store';
import { GraphNode } from './GraphNode';
import { GraphLink } from './GraphLink';

export function GraphVisualizer() {
  const { nodes, links, onNodeClick } = useGraphStore();
  
  return (
    <div className="graph-visualizer">
      <svg width="100%" height="600">
        {links.map(link => (
          <GraphLink key={`${link.source}-${link.target}`} link={link} />
        ))}
        {nodes.map(node => (
          <GraphNode key={node.id} node={node} onClick={onNodeClick} />
        ))}
      </svg>
    </div>
  );
}